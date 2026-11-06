const axios = require('axios');
const crypto = require('crypto');

/**
 * iTrackSafe / GPS51 Live Telemetry Service for FM XPRESS
 * Connects directly to hardware GPS trackers on FM XPRESS delivery motorcycles.
 */
class ITrackSafeService {
  constructor() {
    this.host = process.env.ITRACKSAFE_HOST || 'https://web.itracksafe.com';
    this.username = process.env.ITRACKSAFE_USERNAME || 'Frankoguche';
    this.password = process.env.ITRACKSAFE_PASSWORD || 'FRoguche49';
    this.token = null;
    this.tokenExpiresAt = 0;
    this.cachedPositions = null;
    this.lastFetchTime = 0;
    this.cacheTtlMs = 4000; // 4 seconds in-memory cache to prevent flooding GPS server
  }

  /**
   * Hashes password using MD5 as required by GPS51 / iTrackSafe authentication
   */
  hashPassword(pwd) {
    return crypto.createHash('md5').update(pwd).digest('hex');
  }

  /**
   * Authenticates with iTrackSafe and caches session token
   */
  async login() {
    try {
      const md5Password = this.hashPassword(this.password);
      const payload = {
        type: 'USER',
        from: 'web',
        username: this.username,
        password: md5Password,
        browser: 'Chrome/104.0.0.0'
      };

      const res = await axios.post(`${this.host}/webapi?action=login`, payload, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      });

      if (res.data && res.data.status === 0 && res.data.token) {
        this.token = res.data.token;
        // Tokens are typically valid for days; refresh every 12 hours
        this.tokenExpiresAt = Date.now() + (12 * 60 * 60 * 1000);
        console.log(`[iTrackSafe] ✅ Authenticated as ${this.username}. Token: ${this.token.substring(0, 8)}...`);
        return this.token;
      } else {
        console.warn('[iTrackSafe] ⚠️ Login failed:', res.data);
        return null;
      }
    } catch (err) {
      console.error('[iTrackSafe] ❌ Login error:', err.message);
      return null;
    }
  }

  /**
   * Ensures an active session token is available
   */
  async ensureToken() {
    if (!this.token || Date.now() >= this.tokenExpiresAt) {
      await this.login();
    }
    return this.token;
  }

  /**
   * Fetches real-time GPS telemetry for all active fleet bikes
   */
  async getAllBikePositions() {
    const now = Date.now();
    if (this.cachedPositions && (now - this.lastFetchTime < this.cacheTtlMs)) {
      return this.cachedPositions;
    }

    const token = await this.ensureToken();
    if (!token) return [];

    try {
      const url = `${this.host}/webapi?action=lastposition&token=${token}&extend=self&serverid=2`;
      const payload = {
        deviceids: [], // Empty array queries all devices assigned to this account
        lastquerypositiontime: -1
      };

      const res = await axios.post(url, payload, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      });

      if (res.data && res.data.status === 0 && Array.isArray(res.data.records)) {
        // Exclude user's private car (Plate RSH394DM / Device 6038133156) from delivery fleet
        const EXCLUDED_DEVICE_IDS = new Set(['6038133156']);

        const bikeRecords = res.data.records.filter(r => !EXCLUDED_DEVICE_IDS.has(String(r.deviceid)));

        const positions = await Promise.all(bikeRecords.map(async (r) => {
          const lat = Number(r.callat);
          const lng = Number(r.callon);
          const currentStreet = await this.resolveStreetName(lat, lng);

          return {
            deviceId: String(r.deviceid),
            vehicleName: 'FM XPRESS Delivery Bike (LD3P CMCP)',
            plateOrChassis: 'LD3P CMCP 2T20 05131',
            lat,
            lng,
            currentStreet,
            speedKmH: Math.round((Number(r.speed) || 0) / 1000), // Speed in km/h
            course: Number(r.course) || 0, // Heading in degrees (0-360)
            altitude: Number(r.altitude) || 0,
            statusText: r.strstatusen || 'Active',
            isAccOn: !Boolean(r.strstatusen && r.strstatusen.toLowerCase().includes('acc off')),
            lastUpdateTime: r.updatetime ? new Date(r.updatetime).toISOString() : new Date().toISOString()
          };
        }));

        this.cachedPositions = positions;
        this.lastFetchTime = now;
        return positions;
      }

      // If token expired, clear token and retry once
      if (res.data && res.data.status !== 0) {
        console.warn('[iTrackSafe] Token may have expired, clearing cache:', res.data.cause);
        this.token = null;
      }

      return this.cachedPositions || [];
    } catch (err) {
      console.error('[iTrackSafe] Error fetching bike positions:', err.message);
      return this.cachedPositions || [];
    }
  }

  /**
   * Returns live position for a specific bike by Device ID or index
   */
  async getBikeLocation(deviceId = null) {
    const all = await this.getAllBikePositions();
    if (!all || all.length === 0) return null;

    if (!deviceId) {
      // Find delivery motorcycle (6038161441)
      const primaryBike = all.find(b => b.deviceId === '6038161441');
      return primaryBike || all[0];
    }

    const cleanTarget = String(deviceId).trim();
    const found = all.find(b => b.deviceId === cleanTarget);
    return found || all[0];
  }

  /**
   * Resolves exact street name from latitude and longitude using Google Reverse Geocode or OpenStreetMap
   */
  async resolveStreetName(lat, lng) {
    if (!lat || !lng) return 'Kubwa, Abuja';
    const key = `${lat.toFixed(4)},${lng.toFixed(4)}`;
    if (!this.streetCache) this.streetCache = new Map();
    if (this.streetCache.has(key)) {
      return this.streetCache.get(key);
    }

    const apiKey = (process.env.GOOGLE_MAPS_API_KEY || '').trim();

    // 1. Google Reverse Geocoding (Gold Standard for Nigerian streets)
    if (apiKey) {
      try {
        const gRes = await axios.get(
          `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=${apiKey}&result_type=street_address|route|neighborhood|sublocality`,
          { timeout: 3500 }
        );
        if (gRes.data && gRes.data.results && gRes.data.results.length > 0) {
          const res = gRes.data.results[0];
          const routeComp = res.address_components.find(c => c.types.includes('route'));
          const sublocalityComp = res.address_components.find(c => c.types.includes('sublocality') || c.types.includes('neighborhood'));

          let street = '';
          if (routeComp && sublocalityComp) {
            street = `${routeComp.long_name}, ${sublocalityComp.long_name}`;
          } else if (routeComp) {
            street = `${routeComp.long_name}, Kubwa`;
          } else {
            const parts = (res.formatted_address || '').split(',');
            street = parts.slice(0, 2).join(', ').trim();
          }

          if (street) {
            this.streetCache.set(key, street);
            return street;
          }
        }
      } catch (err) {
        // Continue to fallback
      }
    }

    // 2. OpenStreetMap Reverse Geocode Fallback
    try {
      const osmRes = await axios.get(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`,
        { headers: { 'User-Agent': 'FMXpressTracker/1.0' }, timeout: 3500 }
      );
      if (osmRes.data && osmRes.data.address) {
        const addr = osmRes.data.address;
        const road = addr.road || addr.pedestrian || addr.cycleway || addr.path || 'Kubwa';
        const area = addr.suburb || addr.neighbourhood || addr.city_district || 'Kubwa';
        const name = road === area ? `${road}, Abuja` : `${road}, ${area}`;
        this.streetCache.set(key, name);
        return name;
      }
    } catch (_) {}

    return 'Kubwa, Abuja';
  }
}

module.exports = new ITrackSafeService();
