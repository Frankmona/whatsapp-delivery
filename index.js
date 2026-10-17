require('dotenv').config();
// FM XPRESS Dispatch & WhatsApp Engine - Dual Engine (Google Routes API + OpenRouteService)
const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const axios = require('axios');
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

const app = express();
// Middleware to parse JSON bodies
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const PORT = process.env.PORT || 3000;

// Customer conversational state tracker
// Key: phone number, Value: { stage: 'AWAITING_PICKUP' | 'AWAITING_DELIVERY', pickup_address, pickup_coords }
const customerSessions = {};
// --- Settings and Fleet Zone Storage ---
function getPricingSettings() {
  try {
    const raw = fs.readFileSync(path.join(__dirname, 'settings.json'), 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    return {
      base_fee: 1500,
      per_km_rate: 200,
      max_pickup_distance_km: 7,
      far_pickup_surcharge: 800,
      allow_far_pickup_with_surcharge: false,
      public_url: process.env.PUBLIC_URL || 'https://wife-minimal-tones-efforts.trycloudflare.com',
      google_maps_api_key: process.env.GOOGLE_MAPS_API_KEY || ''
    };
  }
}

function savePricingSettings(settings) {
  fs.writeFileSync(path.join(__dirname, 'settings.json'), JSON.stringify(settings, null, 2), 'utf8');
}

// Live Rider Station / Zone Management (persisted in rider_zones.json)
const RIDER_ZONES_FILE = path.join(__dirname, 'rider_zones.json');

function getRiderZones() {
  try {
    const raw = fs.readFileSync(RIDER_ZONES_FILE, 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    return { default_zone: 'Kubwa', riders: {} };
  }
}

function saveRiderZones(data) {
  try {
    fs.writeFileSync(RIDER_ZONES_FILE, JSON.stringify(data, null, 2), 'utf8');
  } catch (err) {
    console.error('Failed to save rider zones:', err);
  }
}

function getRiderCurrentZone(riderId) {
  const data = getRiderZones();
  return (data.riders && data.riders[riderId]) || data.default_zone || 'Kubwa';
}

function setRiderCurrentZone(riderId, zoneName) {
  const data = getRiderZones();
  if (!data.riders) data.riders = {};
  data.riders[riderId] = zoneName;
  saveRiderZones(data);
}

function extractDistrictName(address) {
  if (!address) return 'Kubwa';
  const lower = address.toLowerCase();
  const known = [
    'kubwa', 'gwarinpa', 'wuse 2', 'wuse', 'maitama', 'jabi', 'utako', 'garki',
    'apo', 'lugbe', 'lokogoma', 'dawaki', 'dutse', 'life camp', 'asokoro', 'central area'
  ];
  for (const d of known) {
    if (lower.includes(d)) {
      return d.charAt(0).toUpperCase() + d.slice(1);
    }
  }
  return address.split(',')[0].trim();
}

// --- Admin Authentication & Role Management ---
const JWT_SECRET = process.env.JWT_SECRET || process.env.VERIFY_TOKEN || 'fm_xpress_jwt_secret_2026';
const MASTER_ADMIN_EMAIL = (process.env.ADMIN_EMAIL || 'admin@fmxpress.com').toLowerCase().trim();
const MASTER_ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'Admin@FmXpress2026!';

function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha512').toString('hex');
  return `${salt}:${hash}`;
}

function verifyPassword(password, storedHash) {
  if (!storedHash) return false;
  if (!storedHash.includes(':')) {
    return password === storedHash;
  }
  const [salt, originalHash] = storedHash.split(':');
  const hash = crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha512').toString('hex');
  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(originalHash));
}

function generateToken(payload) {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  const body = Buffer.from(JSON.stringify({ ...payload, exp: Date.now() + (14 * 24 * 60 * 60 * 1000) })).toString('base64url');
  const signature = crypto.createHmac('sha256', JWT_SECRET).update(`${header}.${body}`).digest('base64url');
  return `${header}.${body}.${signature}`;
}

function verifyToken(token) {
  if (!token) return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [header, body, signature] = parts;
  const expectedSig = crypto.createHmac('sha256', JWT_SECRET).update(`${header}.${body}`).digest('base64url');
  if (signature !== expectedSig) return null;
  try {
    const payload = JSON.parse(Buffer.from(body, 'base64url').toString('utf8'));
    if (payload.exp && Date.now() > payload.exp) return null;
    return payload;
  } catch (e) {
    return null;
  }
}

function authMiddleware(requiredRole = null) {
  return (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = (authHeader && authHeader.startsWith('Bearer ') ? authHeader.slice(7) : null) || req.query.token;

    if (!token) {
      return res.status(401).json({ success: false, error: 'Authentication required. Please sign in.' });
    }

    const decoded = verifyToken(token);
    if (!decoded) {
      return res.status(401).json({ success: false, error: 'Session expired or invalid. Please sign in again.' });
    }

    req.user = decoded;

    if (requiredRole === 'admin' && decoded.role !== 'admin' && decoded.role !== 'super_admin') {
      return res.status(403).json({ success: false, error: 'Access denied: Requires Administrator role.' });
    }

    next();
  };
}

const ADMIN_USERS_FILE = path.join(__dirname, 'admin_users.json');

function getLocalAdminUsers() {
  try {
    if (fs.existsSync(ADMIN_USERS_FILE)) {
      return JSON.parse(fs.readFileSync(ADMIN_USERS_FILE, 'utf8'));
    }
  } catch (err) {
    console.error('Error reading local admin users file:', err.message);
  }
  return [];
}

function saveLocalAdminUsers(users) {
  try {
    fs.writeFileSync(ADMIN_USERS_FILE, JSON.stringify(users, null, 2), 'utf8');
  } catch (err) {
    console.error('Error saving local admin users file:', err.message);
  }
}

// POST /api/admin/login
app.post('/api/admin/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ success: false, error: 'Email and password are required.' });
    }

    const cleanEmail = email.toLowerCase().trim();

    // 1. Try checking Supabase admin_users table
    try {
      const { data: dbUser } = await supabase
        .from('admin_users')
        .select('*')
        .eq('email', cleanEmail)
        .maybeSingle();

      if (dbUser && verifyPassword(password, dbUser.password_hash)) {
        const token = generateToken({
          id: dbUser.id,
          email: dbUser.email,
          name: dbUser.name,
          role: dbUser.role || 'admin'
        });
        return res.json({
          success: true,
          token,
          user: { id: dbUser.id, email: dbUser.email, name: dbUser.name, role: dbUser.role || 'admin' }
        });
      }
    } catch (dbErr) {
      console.warn('[Admin Auth] Supabase lookup note:', dbErr.message);
    }

    // 2. Check Local File Fallback
    const localUsers = getLocalAdminUsers();
    const localMatch = localUsers.find(u => u.email === cleanEmail);
    if (localMatch && verifyPassword(password, localMatch.password_hash)) {
      const token = generateToken({
        id: localMatch.id,
        email: localMatch.email,
        name: localMatch.name,
        role: localMatch.role || 'dispatcher'
      });
      return res.json({
        success: true,
        token,
        user: { id: localMatch.id, email: localMatch.email, name: localMatch.name, role: localMatch.role || 'dispatcher' }
      });
    }

    // 3. Check Master Admin Credentials (fallback)
    if (cleanEmail === MASTER_ADMIN_EMAIL && (password === MASTER_ADMIN_PASSWORD || verifyPassword(password, hashPassword(MASTER_ADMIN_PASSWORD)))) {
      const token = generateToken({
        id: 'super-admin-01',
        email: MASTER_ADMIN_EMAIL,
        name: 'Lead Dispatch Admin',
        role: 'super_admin'
      });
      return res.json({
        success: true,
        token,
        user: { id: 'super-admin-01', email: MASTER_ADMIN_EMAIL, name: 'Lead Dispatch Admin', role: 'super_admin' }
      });
    }

    return res.status(401).json({ success: false, error: 'Invalid email or password.' });
  } catch (err) {
    console.error('[Admin Login Error]:', err.message);
    res.status(500).json({ success: false, error: 'An error occurred during authentication.' });
  }
});

// GET /api/admin/me
app.get('/api/admin/me', authMiddleware(), (req, res) => {
  res.json({ success: true, user: req.user });
});

// GET /api/admin/users
app.get('/api/admin/users', authMiddleware('admin'), async (req, res) => {
  try {
    let dbUsers = [];
    try {
      const { data, error } = await supabase
        .from('admin_users')
        .select('id, email, name, role, created_at')
        .order('created_at', { ascending: false });
      if (!error && data) dbUsers = data;
    } catch (dbErr) {
      // Supabase table not created yet
    }

    const localUsers = getLocalAdminUsers().map(u => ({
      id: u.id,
      email: u.email,
      name: u.name,
      role: u.role,
      created_at: u.created_at
    }));

    // Merge and deduplicate by email
    const all = [...dbUsers];
    for (const u of localUsers) {
      if (!all.find(x => x.email === u.email)) all.push(u);
    }

    // Always include Master Admin
    if (!all.find(x => x.email === MASTER_ADMIN_EMAIL)) {
      all.unshift({
        id: 'super-admin-01',
        email: MASTER_ADMIN_EMAIL,
        name: 'Lead Dispatch Admin',
        role: 'super_admin',
        created_at: new Date().toISOString()
      });
    }

    res.json({ success: true, users: all });
  } catch (err) {
    res.json({
      success: true,
      users: [
        { id: 'super-admin-01', email: MASTER_ADMIN_EMAIL, name: 'Lead Dispatch Admin', role: 'super_admin', created_at: new Date().toISOString() }
      ]
    });
  }
});

// POST /api/admin/users
app.post('/api/admin/users', authMiddleware('admin'), async (req, res) => {
  try {
    const { email, password, name, role } = req.body;
    if (!email || !password || !name) {
      return res.status(400).json({ success: false, error: 'Email, name, and password are required.' });
    }

    const cleanEmail = email.toLowerCase().trim();
    const password_hash = hashPassword(password);
    const assignedRole = ['super_admin', 'admin', 'dispatcher'].includes(role) ? role : 'dispatcher';

    // 1. Try Supabase insert
    try {
      const { data, error } = await supabase
        .from('admin_users')
        .insert([{ email: cleanEmail, password_hash, name: name.trim(), role: assignedRole }])
        .select('id, email, name, role, created_at');

      if (!error && data && data.length > 0) {
        return res.json({ success: true, user: data[0] });
      }
    } catch (dbErr) {
      console.warn('[Admin Create User] Falling back to local storage:', dbErr.message);
    }

    // 2. Local fallback storage
    const localUsers = getLocalAdminUsers();
    if (localUsers.find(u => u.email === cleanEmail) || cleanEmail === MASTER_ADMIN_EMAIL) {
      return res.status(400).json({ success: false, error: 'A staff user with this email already exists.' });
    }

    const newUser = {
      id: 'usr_' + Date.now(),
      email: cleanEmail,
      password_hash,
      name: name.trim(),
      role: assignedRole,
      created_at: new Date().toISOString()
    };

    localUsers.push(newUser);
    saveLocalAdminUsers(localUsers);

    res.json({
      success: true,
      user: { id: newUser.id, email: newUser.email, name: newUser.name, role: newUser.role, created_at: newUser.created_at }
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// DELETE /api/admin/users/:id
app.delete('/api/admin/users/:id', authMiddleware('admin'), async (req, res) => {
  try {
    const { id } = req.params;
    if (id === 'super-admin-01') {
      return res.status(400).json({ success: false, error: 'Cannot delete the master super admin account.' });
    }

    try {
      await supabase.from('admin_users').delete().eq('id', id);
    } catch (dbErr) {
      // ignore if table not present
    }

    let localUsers = getLocalAdminUsers();
    localUsers = localUsers.filter(u => u.id !== id);
    saveLocalAdminUsers(localUsers);

    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// --- Web Portal / Admin Dashboard Endpoints ---
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});

app.get('/api/settings', authMiddleware('admin'), (req, res) => {
  res.json(getPricingSettings());
});

app.post('/api/settings', authMiddleware('admin'), (req, res) => {
  try {
    const { 
      base_fee, 
      per_km_rate, 
      max_pickup_distance_km, 
      far_pickup_surcharge, 
      allow_far_pickup_with_surcharge,
      public_url,
      google_maps_api_key
    } = req.body;
    
    const current = getPricingSettings();
    if (base_fee !== undefined && !isNaN(Number(base_fee))) {
      current.base_fee = Number(base_fee);
    }
    if (per_km_rate !== undefined && !isNaN(Number(per_km_rate))) {
      current.per_km_rate = Number(per_km_rate);
    }
    if (max_pickup_distance_km !== undefined && !isNaN(Number(max_pickup_distance_km))) {
      current.max_pickup_distance_km = Number(max_pickup_distance_km);
    }
    if (far_pickup_surcharge !== undefined && !isNaN(Number(far_pickup_surcharge))) {
      current.far_pickup_surcharge = Number(far_pickup_surcharge);
    }
    if (allow_far_pickup_with_surcharge !== undefined) {
      current.allow_far_pickup_with_surcharge = Boolean(allow_far_pickup_with_surcharge);
    }
    if (public_url) {
      current.public_url = public_url.trim().replace(/\/+$/, '');
    }
    if (google_maps_api_key !== undefined) {
      current.google_maps_api_key = google_maps_api_key.trim();
    }

    savePricingSettings(current);
    console.log(`[Settings Updated] Base: ₦${current.base_fee}, Rate: ₦${current.per_km_rate}/km, MaxRadius: ${current.max_pickup_distance_km}km, Surcharge: ₦${current.far_pickup_surcharge}`);
    res.json({ success: true, settings: current });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Live route test endpoint for admin to verify routing and pricing
app.get('/api/test-route', async (req, res) => {
  try {
    const pickup = req.query.pickup || 'Wuse 2, Abuja';
    const delivery = req.query.delivery || 'Gwarinpa, Abuja';

    // 1. Try Google Maps first (Gold Standard)
    const googleRes = await getGoogleMapsDistance(pickup, delivery);
    if (googleRes) {
      const pricing = getPricingSettings();
      const calculatedPrice = pricing.base_fee + (googleRes.distanceKm * pricing.per_km_rate);
      return res.json({
        success: true,
        source: 'Google Maps Matrix (Live)',
        pickup: googleRes.pickupResolved,
        delivery: googleRes.deliveryResolved,
        distanceKm: googleRes.distanceKm,
        duration: googleRes.durationText,
        pricing,
        calculatedPrice
      });
    }

    // 2. Fallback to OpenRouteService + Local Abuja Knowledge Base
    const pickupRes = await getCoordinatesWithDetails(pickup);
    const deliveryRes = await getCoordinatesWithDetails(delivery);

    if (!pickupRes || !deliveryRes) {
      return res.status(400).json({
        success: false,
        error: `Could not geocode address: ${!pickupRes ? pickup : delivery}`
      });
    }

    const distanceMeters = await getDrivingDistance(pickupRes.coords, deliveryRes.coords);
    if (!distanceMeters) {
      return res.status(400).json({
        success: false,
        error: 'Could not map drivable route between those locations.'
      });
    }

    const distanceKm = Number((distanceMeters / 1000).toFixed(1));
    const pricing = getPricingSettings();
    const calculatedPrice = pricing.base_fee + (distanceKm * pricing.per_km_rate);

    res.json({
      success: true,
      source: 'OpenRouteService (Fallback)',
      pickup: pickupRes.label,
      delivery: deliveryRes.label,
      distanceKm,
      pricing,
      calculatedPrice
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Public endpoint for website tracking widget
app.get('/api/track/:reference', async (req, res) => {
  try {
    const { reference } = req.params;
    const { data: orders, error } = await supabase
      .from('orders')
      .select('id, paystack_reference, pickup_address, delivery_address, status, price_ngn, distance_km, created_at, riders(name, phone_number)')
      .eq('paystack_reference', reference.trim())
      .limit(1);

    if (error || !orders || orders.length === 0) {
      return res.status(404).json({ success: false, error: 'Order reference not found.' });
    }

    const order = orders[0];
    res.json({
      success: true,
      order: {
        reference: order.paystack_reference,
        pickup: order.pickup_address,
        delivery: order.delivery_address,
        status: order.status,
        distanceKm: order.distance_km,
        price: order.price_ngn,
        createdAt: order.created_at,
        rider: order.riders ? { name: order.riders.name, phone: order.riders.phone_number } : null
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

app.get('/api/test-places', async (req, res) => {
  try {
    const input = req.query.input || 'igbenidion cresent kubwa';
    const apiKey = (req.query.key || process.env.GOOGLE_MAPS_API_KEY || getPricingSettings().google_maps_api_key || '').trim();
    console.log(`[Testing Places API with key: ${apiKey.substring(0, 10)}...]`);
    
    // Call Google Places API (New) Autocomplete
    const gRes = await axios.post(
      'https://places.googleapis.com/v1/places:autocomplete',
      {
        input: input,
        includedRegionCodes: ['ng'],
        locationBias: {
          circle: {
            center: { latitude: 9.0765, longitude: 7.3986 },
            radius: 50000.0
          }
        }
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'X-Goog-Api-Key': apiKey
        },
        timeout: 7000
      }
    );
    res.json(gRes.data);
  } catch (err) {
    console.error('[Places API Error]:', err.response ? err.response.data : err.message);
    res.status(500).json({ error: err.response ? err.response.data : err.message });
  }
});

app.get('/api/stats', authMiddleware(), async (req, res) => {
  try {
    const { data: orders } = await supabase.from('orders').select('price_ngn, status');
    const { data: riders } = await supabase.from('riders').select('status');

    let totalRevenue = 0;
    let inTransitCount = 0;
    let deliveredCount = 0;

    (orders || []).forEach(o => {
      if (o.status === 'paid' || o.status === 'delivered') {
        totalRevenue += (Number(o.price_ngn) || 0);
      }
      if (o.status === 'paid') inTransitCount++;
      if (o.status === 'delivered') deliveredCount++;
    });

    const availableRidersCount = (riders || []).filter(r => r.status === 'available').length;
    const isDispatcher = req.user && req.user.role === 'dispatcher';

    res.json({
      totalRevenue: isDispatcher ? null : totalRevenue,
      inTransitCount,
      deliveredCount,
      availableRidersCount,
      userRole: req.user ? req.user.role : 'admin'
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/orders', authMiddleware(), async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('orders')
      .select('*, riders(name, phone_number)')
      .order('created_at', { ascending: false })
      .limit(50);
    if (error) throw error;
    res.json(data || []);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/riders', authMiddleware(), async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('riders')
      .select('*')
      .order('name', { ascending: true });
    if (error) throw error;
    const enriched = (data || []).map(r => ({
      ...r,
      current_zone: getRiderCurrentZone(r.id)
    }));
    res.json(enriched);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/riders', authMiddleware(), async (req, res) => {
  try {
    const { name, phone_number, current_zone } = req.body;
    if (!name || !phone_number) {
      return res.status(400).json({ error: 'Name and phone number are required.' });
    }
    const { data, error } = await supabase
      .from('riders')
      .insert([{ name, phone_number, status: 'available' }])
      .select();
    if (error) throw error;
    const newRider = data[0];
    if (current_zone) {
      setRiderCurrentZone(newRider.id, current_zone);
    }
    res.json({ ...newRider, current_zone: getRiderCurrentZone(newRider.id) });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.put('/api/riders/:id', authMiddleware(), async (req, res) => {
  try {
    const { id } = req.params;
    const { name, phone_number, status, current_zone } = req.body;
    const updateData = {};
    if (name) updateData.name = name;
    if (phone_number) updateData.phone_number = phone_number;
    if (status) updateData.status = status;

    if (current_zone) {
      setRiderCurrentZone(id, current_zone);
    }

    let updatedRider = null;
    if (Object.keys(updateData).length > 0) {
      const { data, error } = await supabase
        .from('riders')
        .update(updateData)
        .eq('id', id)
        .select();
      if (error) throw error;
      updatedRider = data[0];
    } else {
      const { data } = await supabase.from('riders').select('*').eq('id', id).maybeSingle();
      updatedRider = data;
    }

    res.json({ ...updatedRider, current_zone: getRiderCurrentZone(id) });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/riders/:id', authMiddleware('admin'), async (req, res) => {
  try {
    const { id } = req.params;
    // Unlink any orders referencing this rider first so deletion succeeds
    await supabase.from('orders').update({ rider_id: null }).eq('rider_id', id);
    const { error } = await supabase.from('riders').delete().eq('id', id);
    if (error) throw error;
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 1. Basic health check / root redirects to admin portal
app.get('/', (req, res) => {
  res.redirect('/admin');
});

// 2. Webhook verification endpoint (Required by Meta)
app.get('/webhook', (req, res) => {
  const verify_token = process.env.VERIFY_TOKEN;

  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode && token) {
    if (mode === 'subscribe' && token === verify_token) {
      console.log('WEBHOOK_VERIFIED');
      res.status(200).send(challenge);
    } else {
      // Responds with '403 Forbidden' if verify tokens do not match
      res.sendStatus(403);
    }
  } else {
    res.status(400).send('Missing mode or token');
  }
});

// --- Local Abuja Landmark & Phase Coordinate Dictionary ---
// Gives pin-point accuracy for local phases, estates, and zones that OpenStreetMap lacks
const ABUJA_LOCAL_LANDMARKS = [
  { regex: /reggy\s*emmanuel/i, coords: [7.3235, 9.1585], label: "Reggy Emmanuel Rd, Kubwa, Abuja" },
  { regex: /(igbenidion|igbinedion)/i, coords: [7.3385, 9.1455], label: "9 E.O Igbinedion Cres, Kubwa, Abuja" },
  { regex: /(phase\s*4|4th\s*phase).*(kubwa)|(kubwa).*(phase\s*4|4th\s*phase)/i, coords: [7.3235, 9.1585], label: "Phase 4, Kubwa, Abuja" },
  { regex: /(phase\s*3|3rd\s*phase).*(kubwa)|(kubwa).*(phase\s*3|3rd\s*phase)/i, coords: [7.3350, 9.1520], label: "Phase 3, Kubwa, Abuja" },
  { regex: /(phase\s*2|2nd\s*phase).*(kubwa)|(kubwa).*(phase\s*2|2nd\s*phase)/i, coords: [7.3400, 9.1480], label: "Phase 2, Kubwa, Abuja" },
  { regex: /(phase\s*1|1st\s*phase).*(kubwa)|(kubwa).*(phase\s*1|1st\s*phase)/i, coords: [7.3450, 9.1450], label: "Phase 1, Kubwa, Abuja" },
  { regex: /(f01|fo1|f\.o\.1|f\.0\.1|fha|apo\s*1).*(kubwa)|(kubwa).*(f01|fo1|f\.o\.1|f\.0\.1|fha|apo\s*1)|^apo\s*1\s*,?\s*kubwa/i, coords: [7.3385, 9.1455], label: "F01 / FHA / Apo 1, Kubwa, Abuja" },
  { regex: /(pw|p\.w\.).*(kubwa)|(kubwa).*(pw|p\.w\.)/i, coords: [7.3450, 9.1550], label: "PW, Kubwa, Abuja" },
  { regex: /(arab\s*road).*(kubwa)|(kubwa).*(arab\s*road)/i, coords: [7.3550, 9.1350], label: "Arab Road, Kubwa, Abuja" },
  { regex: /(byazhin).*(kubwa)|(kubwa).*(byazhin)/i, coords: [7.3150, 9.1700], label: "Byazhin, Kubwa, Abuja" },
  { regex: /(general\s*hospital).*(kubwa)|(kubwa).*(general\s*hospital)/i, coords: [7.3409, 9.1574], label: "Kubwa General Hospital, Abuja" },
  { regex: /(kubwa\s*market|village).*(kubwa)|(kubwa).*(market|village)/i, coords: [7.3320, 9.1620], label: "Kubwa Village / Market, Abuja" },
  { regex: /^kubwa$/i, coords: [7.3385, 9.1520], label: "Kubwa, Abuja" },

  // Gwarinpa Avenues & Estates
  { regex: /(1st\s*ave|first\s*ave).*(gwarinpa)|(gwarinpa).*(1st\s*ave|first\s*ave)/i, coords: [7.4100, 9.1050], label: "1st Avenue, Gwarinpa, Abuja" },
  { regex: /(2nd\s*ave|second\s*ave).*(gwarinpa)|(gwarinpa).*(2nd\s*ave|second\s*ave)/i, coords: [7.4150, 9.1100], label: "2nd Avenue, Gwarinpa, Abuja" },
  { regex: /(3rd\s*ave|third\s*ave).*(gwarinpa)|(gwarinpa).*(3rd\s*ave|third\s*ave)/i, coords: [7.4200, 9.1150], label: "3rd Avenue, Gwarinpa, Abuja" },
  { regex: /(4th\s*ave|fourth\s*ave).*(gwarinpa)|(gwarinpa).*(4th\s*ave|fourth\s*ave)/i, coords: [7.4280, 9.1220], label: "4th Avenue, Gwarinpa, Abuja" },
  { regex: /(5th\s*ave|fifth\s*ave).*(gwarinpa)|(gwarinpa).*(5th\s*ave|fifth\s*ave)/i, coords: [7.4320, 9.1250], label: "5th Avenue, Gwarinpa, Abuja" },
  { regex: /(6th\s*ave|sixth\s*ave).*(gwarinpa)|(gwarinpa).*(6th\s*ave|sixth\s*ave)/i, coords: [7.4350, 9.1280], label: "6th Avenue, Gwarinpa, Abuja" },
  { regex: /(charlie\s*boy).*(gwarinpa)|(gwarinpa).*(charlie\s*boy)/i, coords: [7.4050, 9.0980], label: "Charlie Boy Bus Stop, Gwarinpa, Abuja" },
  { regex: /^gwarinpa$/i, coords: [7.4180, 9.1120], label: "Gwarinpa Estate, Abuja" },

  // Wuse 2 & Wuse
  { regex: /(aminu\s*kano).*(wuse)|(wuse).*(aminu\s*kano)/i, coords: [7.4750, 9.0750], label: "Aminu Kano Crescent, Wuse 2, Abuja" },
  { regex: /(banex).*(wuse)|(wuse).*(banex)|banex/i, coords: [7.4650, 9.0820], label: "Banex Plaza, Wuse 2, Abuja" },
  { regex: /wuse\s*2/i, coords: [7.4720, 9.0730], label: "Wuse 2, Abuja" },
  { regex: /wuse\s*(zone\s*\d+|market)?/i, coords: [7.4600, 9.0600], label: "Wuse, Abuja" },

  // Maitama
  { regex: /maitama/i, coords: [7.4950, 9.0880], label: "Maitama, Abuja" },

  // Jabi & Utako
  { regex: /(jabi\s*lake\s*mall)|(jabi.*mall)/i, coords: [7.4260, 9.0730], label: "Jabi Lake Mall, Jabi, Abuja" },
  { regex: /jabi/i, coords: [7.4300, 9.0680], label: "Jabi District, Abuja" },
  { regex: /utako/i, coords: [7.4420, 9.0620], label: "Utako District, Abuja" },

  // Garki
  { regex: /garki\s*(area\s*\d+)?/i, coords: [7.4900, 9.0300], label: "Garki, Abuja" },

  // Apo
  { regex: /apo\s*(resettlement|legislative|mechanic|novare)?/i, coords: [7.5050, 8.9950], label: "Apo District, Abuja" },

  // Lugbe
  { regex: /lugbe/i, coords: [7.3750, 8.9750], label: "Lugbe, Airport Road, Abuja" },

  // Life Camp
  { regex: /life\s*camp/i, coords: [7.4050, 9.0650], label: "Life Camp, Abuja" },

  // Lokogoma
  { regex: /lokogoma/i, coords: [7.4550, 8.9850], label: "Lokogoma, Abuja" },

  // Dawaki
  { regex: /dawaki/i, coords: [7.3850, 9.1350], label: "Dawaki, Abuja" },

  // Dutse
  { regex: /dutse\s*(alhaj[i]?)?/i, coords: [7.3650, 9.1550], label: "Dutse Alhaji, Abuja" },

  // Central Area / CBD
  { regex: /(central\s*(area|business\s*district)|cbd|national\s*mosque)/i, coords: [7.4900, 9.0550], label: "Central Business District, Abuja" }
];

// --- Enhanced Helper Functions for Distance & Resilient Geocoding in Nigeria ---
function cleanAddressForGeocoding(rawAddress) {
  if (!rawAddress) return '';
  return rawAddress
    .replace(/^(no\.?|plot|house|flat|block|suite)\s*\d+[\w\/-]*\s*,?\s*/i, '') // strip "No. 4", "Plot 12"
    .replace(/,/g, ' ') // replace commas with space so Pelias doesn't misparse boundaries
    .replace(/[#]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function formatNigerianQuery(addr) {
  let clean = (addr || '').trim();
  if (!clean) return 'Abuja, Nigeria';
  if (!clean.toLowerCase().includes('nigeria')) {
    if (!clean.toLowerCase().includes('abuja')) {
      clean += ', Abuja, Nigeria';
    } else {
      clean += ', Nigeria';
    }
  }
  return clean;
}

async function getCoordinatesWithDetails(address) {
  const apiKey = process.env.OPENROUTESERVICE_API_KEY;
  if (!address) return null;

  const cleaned = cleanAddressForGeocoding(address);

  // 1. Check local Abuja landmark and phase dictionary first for pinpoint accuracy
  for (const item of ABUJA_LOCAL_LANDMARKS) {
    if (item.regex.test(address) || item.regex.test(cleaned)) {
      console.log(`[Local Geocode] Matched "${address}" -> ${item.label} [${item.coords}]`);
      return { coords: item.coords, label: item.label };
    }
  }

  // 2. Check Google Maps Geocoding API if key is available
  const googleKey = (process.env.GOOGLE_MAPS_API_KEY || getPricingSettings().google_maps_api_key || '').trim();
  if (googleKey) {
    try {
      const gRes = await axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
        params: {
          address: formatNigerianQuery(address),
          region: 'ng',
          key: googleKey
        },
        timeout: 7000
      });
      if (gRes.data && gRes.data.status === 'OK' && gRes.data.results && gRes.data.results.length > 0) {
        const topResult = gRes.data.results[0];
        const lat = topResult.geometry.location.lat;
        const lng = topResult.geometry.location.lng;
        console.log(`[Google Geocode] "${address}" -> ${topResult.formatted_address} [${lng}, ${lat}]`);
        return {
          coords: [lng, lat],
          label: topResult.formatted_address || address
        };
      }
    } catch (e) {
      console.warn('[Google Geocode Notice]:', e.message);
    }
  }

  if (!apiKey) return null;
  
  // 2. OpenRouteService geocoding queries in order of specificity
  const queriesToTry = [
    cleaned,
    `${cleaned} Abuja Nigeria`,
    `${cleaned} Nigeria`,
    address
  ];

  for (const query of queriesToTry) {
    if (!query) continue;
    try {
      const res = await axios.get(`https://api.openrouteservice.org/geocode/search`, {
        params: { 
          api_key: apiKey, 
          text: query,
          'boundary.country': 'NGA',
          size: 3
        },
        timeout: 7000
      });
      if (res.data && res.data.features && res.data.features.length > 0) {
        const feature = res.data.features[0];
        const [lon, lat] = feature.geometry.coordinates;
        const label = feature.properties.label || feature.properties.name || address;
        return { coords: [lon, lat], label };
      }
    } catch (err) {
      // Continue to next query candidate
    }
  }

  // Fallback: Check if a known Abuja district or area is mentioned in the text
  const knownDistricts = [
    'kubwa', 'wuse', 'gwarinpa', 'maitama', 'jabi', 'garki', 'utako', 'apo',
    'lugbe', 'asokoro', 'bwari', 'lokogoma', 'dawaki', 'dutse', 'karu', 'nyanya',
    'life camp', 'mpape', 'guzape', 'kado', 'mabushi', 'central area', 'area 1',
    'area 2', 'area 3', 'area 8', 'area 10', 'area 11'
  ];

  const lower = address.toLowerCase();
  for (const district of knownDistricts) {
    if (lower.includes(district)) {
      try {
        const res = await axios.get(`https://api.openrouteservice.org/geocode/search`, {
          params: {
            api_key: apiKey,
            text: `${district}, Abuja, Nigeria`,
            'boundary.country': 'NGA',
            size: 1
          },
          timeout: 7000
        });
        if (res.data && res.data.features && res.data.features.length > 0) {
          const feature = res.data.features[0];
          return {
            coords: feature.geometry.coordinates,
            label: `${address} (resolved via ${district.toUpperCase()}, Abuja)`
          };
        }
      } catch (e) {}
    }
  }

  return null;
}

function resolveAbujaAddress(address) {
  if (!address) return address;
  const cleaned = cleanAddressForGeocoding(address);
  for (const item of ABUJA_LOCAL_LANDMARKS) {
    if (item.regex.test(address) || item.regex.test(cleaned)) {
      return item.label;
    }
  }
  return address;
}

// --- Google Places Autocomplete (New API) ---
async function getGooglePlacesSuggestions(input) {
  const apiKey = (process.env.GOOGLE_MAPS_API_KEY || getPricingSettings().google_maps_api_key || '').trim();
  if (!apiKey || !input || input.trim().length < 3) return [];

  try {
    const res = await axios.post(
      'https://places.googleapis.com/v1/places:autocomplete',
      {
        input: input.trim(),
        includedRegionCodes: ['ng'],
        locationBias: {
          circle: {
            center: { latitude: 9.0765, longitude: 7.3986 }, // Abuja Center
            radius: 50000.0
          }
        }
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'X-Goog-Api-Key': apiKey
        },
        timeout: 5000
      }
    );

    if (res.data && res.data.suggestions && res.data.suggestions.length > 0) {
      const places = [];
      for (const s of res.data.suggestions) {
        if (s.placePrediction && s.placePrediction.text) {
          places.push({
            placeId: s.placePrediction.placeId,
            description: s.placePrediction.text.text,
            mainText: s.placePrediction.structuredFormat?.mainText?.text || s.placePrediction.text.text,
            secondaryText: s.placePrediction.structuredFormat?.secondaryText?.text || ''
          });
        }
      }
      return places.slice(0, 3);
    }
  } catch (err) {
    console.warn('[Places Autocomplete Notice]:', err.response?.data?.error?.message || err.message);
  }
  return [];
}

// --- Google Maps Routing Engine (Supports Google Routes API & Distance Matrix) ---
async function getGoogleMapsDistance(pickup, delivery) {
  const apiKey = (process.env.GOOGLE_MAPS_API_KEY || getPricingSettings().google_maps_api_key || '').trim();
  if (!apiKey) return null;

  // Canonicalize local landmarks & common misspellings first (e.g. "igbenidion cresent" -> "9 E.O Igbinedion Cres, Kubwa")
  const resolvedPickup = resolveAbujaAddress(pickup);
  const resolvedDelivery = resolveAbujaAddress(delivery);

  // Prioritize canonical/resolved queries so misspellings are corrected before Google Routes searches
  const candidatePairs = [
    { p: formatNigerianQuery(resolvedPickup), d: formatNigerianQuery(resolvedDelivery), pRes: resolvedPickup, dRes: resolvedDelivery },
    { p: formatNigerianQuery(pickup), d: formatNigerianQuery(delivery), pRes: pickup, dRes: delivery }
  ];

  // 1. Try Google's Modern Routes API
  for (const pair of candidatePairs) {
    try {
      const routesRes = await axios.post(
        'https://routes.googleapis.com/directions/v2:computeRoutes',
        {
          origin: { address: pair.p },
          destination: { address: pair.d },
          travelMode: 'DRIVE'
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': apiKey,
            'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'
          },
          timeout: 8000
        }
      );

      if (routesRes.data && routesRes.data.routes && routesRes.data.routes.length > 0) {
        const topRoute = routesRes.data.routes[0];
        const distanceMeters = topRoute.distanceMeters;
        const distanceKm = Number((distanceMeters / 1000).toFixed(1));
        const durationSec = parseInt(topRoute.duration || '0', 10);
        const durationText = durationSec > 0 ? `${Math.round(durationSec / 60)} mins` : '';

        // Intra-district sanity safeguard:
        // If pickup and delivery are explicitly in the same district (e.g. Kubwa to Kubwa), distance cannot exceed 15 km!
        const pickupDist = extractDistrictName(pickup).toLowerCase();
        const deliveryDist = extractDistrictName(delivery).toLowerCase();
        if (pickupDist && deliveryDist && pickupDist === deliveryDist && distanceKm > 15) {
          console.warn(`[Route Safeguard Rejected] Intra-district trip (${pickupDist} -> ${deliveryDist}) calculated to ${distanceKm} km. Discarding detour match and trying next pair.`);
          continue;
        }

        console.log(`[Google Routes API] "${pair.pRes}" -> "${pair.dRes}": ${distanceKm} km (${durationText})`);
        return {
          distanceMeters,
          distanceKm,
          durationText,
          pickupResolved: pair.pRes,
          deliveryResolved: pair.dRes
        };
      }
    } catch (err) {
      console.warn(`[Google Routes API Notice for "${pair.p}" -> "${pair.d}"]:`, err.response ? (err.response.data?.error?.message || JSON.stringify(err.response.data)) : err.message);
    }
  }

  // 2. Try classic Google Maps Distance Matrix API
  try {
    const res = await axios.get('https://maps.googleapis.com/maps/api/distancematrix/json', {
      params: {
        origins: originQuery,
        destinations: destQuery,
        mode: 'driving',
        region: 'ng',
        key: apiKey
      },
      timeout: 8000
    });

    if (res.data && res.data.status === 'OK' && res.data.rows && res.data.rows[0].elements[0].status === 'OK') {
      const element = res.data.rows[0].elements[0];
      const distanceMeters = element.distance.value;
      const durationText = element.duration.text;
      const distanceKm = Number((distanceMeters / 1000).toFixed(1));
      const originResolved = res.data.origin_addresses[0] || pickup;
      const destinationResolved = res.data.destination_addresses[0] || delivery;

      console.log(`[Google Maps Matrix] "${pickup}" -> "${delivery}": ${distanceKm} km (${durationText})`);
      return {
        distanceMeters,
        distanceKm,
        durationText,
        pickupResolved: originResolved,
        deliveryResolved: destinationResolved
      };
    } else {
      console.warn(`[Google Maps Matrix Notice] Status: ${res.data?.status}, Element: ${res.data?.rows?.[0]?.elements?.[0]?.status}`);
    }
  } catch (err) {
    console.error('[Google Maps Error]:', err.response ? err.response.data : err.message);
  }
  return null;
}

// Straight-line distance calculation in km (Haversine formula)
function calculateHaversineKm(coords1, coords2) {
  if (!coords1 || !coords2) return 0;
  const [lon1, lat1] = coords1;
  const [lon2, lat2] = coords2;
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

// Backwards-compatible coordinate helper
async function getCoordinates(address) {
  const result = await getCoordinatesWithDetails(address);
  return result ? result.coords : null;
}

async function getDrivingDistance(coords1, coords2) {
  const haversineKm = calculateHaversineKm(coords1, coords2);

  try {
    const res = await axios.get(`https://api.openrouteservice.org/v2/directions/driving-car`, {
      params: {
        api_key: process.env.OPENROUTESERVICE_API_KEY,
        start: `${coords1[0]},${coords1[1]}`,
        end: `${coords2[0]},${coords2[1]}`
      },
      timeout: 8000
    });
    // Returns distance in meters
    const orsMeters = res.data.features[0].properties.summary.distance;
    const orsKm = orsMeters / 1000;

    // OpenStreetMap Median-Barrier / Expressway Detour Correction:
    // In Nigerian cities, OpenStreetMap often lacks small local neighborhood links or has highway median
    // barriers that force artificial 6-8 km U-turn loops for passenger cars.
    // Dispatch riders on motorcycles use local collector roads and direct neighborhood links.
    // If ORS road distance is > 1.8x straight-line for local intra-city trips (< 15 km):
    if (haversineKm < 15 && orsKm > (1.8 * haversineKm)) {
      const realisticKm = Math.round(haversineKm * 1.5 * 10) / 10;
      console.log(`[Route Calibrated] ORS detour of ${orsKm.toFixed(1)} km corrected to local motorbike route of ${realisticKm} km (straight-line: ${haversineKm.toFixed(1)} km)`);
      return Math.round(realisticKm * 1000);
    }

    return orsMeters;
  } catch (error) {
    console.error("Routing error, using calibrated straight-line distance:", error.message);
    const fallbackKm = Math.max(1.0, Math.round(haversineKm * 1.5 * 10) / 10);
    return Math.round(fallbackKm * 1000);
  }
}

// --- Helper Functions for Paystack Payments ---
async function generatePaystackLink(amountNGN, email, reference) {
  try {
    const secretKey = (process.env.PAYSTACK_SECRET_KEY || '').trim();
    const settings = getPricingSettings();
    const publicUrl = (settings.public_url || process.env.PUBLIC_URL || 'https://wife-minimal-tones-efforts.trycloudflare.com').replace(/\/+$/, '');
    const callbackUrl = `${publicUrl}/payment-callback`;
    
    console.log(`[Paystack Initialize] Amount: ₦${amountNGN}, Callback: ${callbackUrl}`);

    const res = await axios.post('https://api.paystack.co/transaction/initialize', {
      amount: Math.round(amountNGN * 100), // Paystack requires amount in kobo
      email: email, 
      reference: reference,
      callback_url: callbackUrl
    }, {
      headers: {
        Authorization: `Bearer ${secretKey}`,
        'Content-Type': 'application/json'
      }
    });
    return res.data.data.authorization_url;
  } catch (error) {
    console.error("Paystack error:", error.response ? error.response.data : error.message);
    return null;
  }
}

// --- WhatsApp Interactive Messaging Helpers ---
async function sendWhatsAppInteractiveMenu(to) {
  const bodyText = `👋 Welcome to *FM XPRESS*! 🏍️\n\nFast & reliable dispatch delivery across Abuja.\n\nHow can we help you today?`;
  const buttons = [
    { id: 'btn_send_package', title: '📦 Send Package' },
    { id: 'btn_track_order', title: '🔍 Track Order' },
    { id: 'btn_support', title: '💬 Speak to Support' }
  ];

  await sendWhatsAppButtons(to, bodyText, buttons);
}

async function sendWhatsAppButtons(to, bodyText, buttons) {
  const payload = {
    messaging_product: "whatsapp",
    recipient_type: "individual",
    to: to,
    type: "interactive",
    interactive: {
      type: "button",
      body: {
        text: bodyText
      },
      action: {
        buttons: buttons.map(b => ({
          type: "reply",
          reply: {
            id: b.id,
            title: b.title.substring(0, 20)
          }
        }))
      }
    }
  };

  try {
    const res = await axios.post(
      `https://graph.facebook.com/v17.0/${process.env.PHONE_NUMBER_ID}/messages`,
      payload,
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
          "Content-Type": "application/json"
        }
      }
    );
    console.log(`[WhatsApp] Buttons sent to ${to}: ID ${res.data.messages[0].id}`);
  } catch (error) {
    console.error("[WhatsApp] Error sending buttons, sending text fallback:", error.response ? error.response.data : error.message);
    const optionsText = buttons.map((b, i) => `${i + 1}️⃣ ${b.title}`).join('\n');
    await sendWhatsAppMessage(to, `${bodyText}\n\n${optionsText}\n\n👉 *Reply 1, 2, or 3*`);
  }
}

// --- Menu Handlers ---
async function handleSendPackage(from) {
  customerSessions[from] = { stage: 'AWAITING_PICKUP', startedAt: Date.now() };
  const promptText = `📦 *Step 1 of 3: Pickup Location*\n_(e.g. 15 Ademola Adetokunbo Crescent, Wuse 2)_`;
  await sendWhatsAppMessage(from, promptText);
}

async function handleTrackOrder(from) {
  try {
    const { data: orders, error } = await supabase
      .from('orders')
      .select('*, riders(name, phone_number)')
      .eq('customer_phone', from)
      .order('created_at', { ascending: false })
      .limit(1);

    if (error) throw error;

    if (!orders || orders.length === 0) {
      await sendWhatsAppButtons(from, `🔍 *Track Order*\n\nNo active orders found for this WhatsApp number.`, [
        { id: 'btn_send_package', title: '📦 Send Package' },
        { id: 'btn_support', title: '💬 Speak to Support' }
      ]);
      return;
    }

    const order = orders[0];
    const amount = (Number(order.price_ngn) || 0).toLocaleString('en-NG');

    if (order.status === 'pending_payment') {
      await sendWhatsAppMessage(from, `🔍 *Order: ${order.paystack_reference}*\n\n📍 *Pickup:* ${order.pickup_address}\n🏁 *Delivery:* ${order.delivery_address}\n⏳ *Status:* *Awaiting Payment*\n💰 *Amount:* ₦${amount}\n\n💳 Please complete payment to dispatch your rider.\n\n_Reply MENU to start over._`);
    } else if (order.status === 'paid') {
      const riderName = order.riders ? order.riders.name : 'Assigned Rider';
      const riderPhone = order.riders ? order.riders.phone_number : 'Available soon';
      await sendWhatsAppMessage(from, `🔍 *Order: ${order.paystack_reference}*\n\n📍 *Pickup:* ${order.pickup_address}\n🏁 *Delivery:* ${order.delivery_address}\n🏍️ *Status:* *In Transit* 🚀\n👤 *Rider:* ${riderName}\n📞 *Phone:* +${riderPhone}\n\nYour rider is on the way!\n_Reply MENU for main menu._`);
    } else if (order.status === 'delivered') {
      const deliveredBy = order.riders ? order.riders.name : 'FM XPRESS Rider';
      await sendWhatsAppMessage(from, `✅ *Order: ${order.paystack_reference}*\n\n📍 *Pickup:* ${order.pickup_address}\n🏁 *Delivery:* ${order.delivery_address}\n🎉 *Status:* *Delivered*\n👤 *Delivered By:* ${deliveredBy}\n\nThank you for choosing *FM XPRESS*! 🚚\n_Reply MENU to start a new booking._`);
    } else {
      await sendWhatsAppMessage(from, `🔍 *Order: ${order.paystack_reference}*\n\n📍 *Pickup:* ${order.pickup_address}\n🏁 *Delivery:* ${order.delivery_address}\n📌 *Status:* ${order.status.toUpperCase()}`);
    }
  } catch (err) {
    console.error("[Track Order Error]:", err.message);
    await sendWhatsAppMessage(from, "⚠️ Could not retrieve tracking details right now. Please try again shortly.");
  }
}

async function handleGetPrice(from) {
  const pricing = getPricingSettings();
  const price5 = pricing.base_fee + (5 * pricing.per_km_rate);
  const price10 = pricing.base_fee + (10 * pricing.per_km_rate);
  const price20 = pricing.base_fee + (20 * pricing.per_km_rate);

  const priceMsg = `💰 *FM XPRESS Delivery Rates*\n\n` +
    `🏁 *Base Pickup Fee:* ₦${pricing.base_fee.toLocaleString('en-NG')}\n` +
    `🛣️ *Distance Rate:* ₦${pricing.per_km_rate.toLocaleString('en-NG')} per km\n\n` +
    `📊 *Estimated Route Costs:*\n` +
    `• Short distance (~5 km): ₦${price5.toLocaleString('en-NG')}\n` +
    `• Medium distance (~10 km): ₦${price10.toLocaleString('en-NG')}\n` +
    `• Long distance (~20 km): ₦${price20.toLocaleString('en-NG')}\n\n` +
    `💡 *Want an exact price for your package?*\nReply *1* and enter your pickup & delivery addresses for an instant automated quote!`;

  await sendWhatsAppMessage(from, priceMsg);
}

async function handleSupport(from) {
  const supportMsg = `💬 *FM XPRESS Customer Support*\n\n` +
    `Need help with a pickup, tracking, or booking? We're here for you!\n\n` +
    `📞 *Call / Direct WhatsApp:* +234 703 785 8093\n` +
    `📧 *Email:* support@fmxpress.com\n` +
    `⏰ *Operating Hours:* Mon – Sat, 7:00 AM – 8:00 PM\n\n` +
    `_Reply MENU anytime to return to main options._`;

  await sendWhatsAppMessage(from, supportMsg);
}

function matchMenuOption(text) {
  if (!text) return null;
  const t = text.toLowerCase().trim();
  if (t === '1' || t === '1️⃣' || t === 'send' || t === 'send package' || t === 'send a package' || t === 'book') return 'menu_send_package';
  if (t === '2' || t === '2️⃣' || t === 'track' || t === 'track order' || t === 'track my delivery' || t.startsWith('track')) return 'menu_track_order';
  if (t === '3' || t === '3️⃣' || t === 'support' || t === 'speak to support' || t === 'help' || t === 'agent' || t === 'contact' || t === 'call') return 'menu_support';
  if (t === '4' || t === '4️⃣' || t === 'price' || t === 'pricing' || t === 'get price' || t === 'rates' || t === 'rate') return 'menu_get_price';
  return null;
}

// --- Proximity Dispatch: Match closest available rider to pickup ---
async function findBestAvailableRider(pickupAddress) {
  try {
    const { data: riders, error } = await supabase
      .from('riders')
      .select('*')
      .eq('status', 'available');

    if (error || !riders || riders.length === 0) {
      return null;
    }

    const pickupRes = await getCoordinatesWithDetails(pickupAddress);
    const pickupCoords = pickupRes ? pickupRes.coords : [7.3385, 9.1520]; // Default Kubwa

    const scoredRiders = [];
    for (const rider of riders) {
      const zoneName = getRiderCurrentZone(rider.id);
      const zoneRes = await getCoordinatesWithDetails(zoneName);
      const riderCoords = zoneRes ? zoneRes.coords : [7.3385, 9.1520];

      const straightDistKm = calculateHaversineKm(riderCoords, pickupCoords);
      const estimatedRoadKm = Math.round(straightDistKm * 1.5 * 10) / 10;

      scoredRiders.push({
        ...rider,
        current_zone: zoneName,
        distanceToPickupKm: estimatedRoadKm
      });
    }

    scoredRiders.sort((a, b) => a.distanceToPickupKm - b.distanceToPickupKm);
    console.log(`[Proximity Dispatch] Available riders for "${pickupAddress}":`,
      scoredRiders.map(r => `${r.name} in ${r.current_zone} (${r.distanceToPickupKm} km)`).join(', ')
    );

    return scoredRiders[0];
  } catch (err) {
    console.error("[Proximity Dispatch Error]:", err.message);
    const { data } = await supabase.from('riders').select('*').eq('status', 'available').limit(1);
    return data && data[0] ? data[0] : null;
  }
}

// --- Shared Payment Confirmation Handler (Used by Callback and Webhook) ---
async function handleSuccessfulPayment(reference, paidAmount) {
  console.log(`[Payment] Processing payment confirmation for reference: ${reference}`);
  
  try {
    // 1. Fetch the order
    const { data: existingOrders, error: findErr } = await supabase
      .from('orders')
      .select('*, riders(name, phone_number)')
      .eq('paystack_reference', reference);

    if (findErr || !existingOrders || existingOrders.length === 0) {
      console.warn(`[Payment] Order with reference ${reference} not found in database.`);
      return null;
    }

    const existingOrder = existingOrders[0];

    // Idempotency: if already processed, return existing state
    if (existingOrder.status === 'paid' || existingOrder.status === 'delivered') {
      console.log(`[Payment] Order ${reference} already marked as paid.`);
      return { order: existingOrder, rider: existingOrder.riders };
    }

    // 2. Mark order as paid
    const { data: updatedOrders } = await supabase
      .from('orders')
      .update({ status: 'paid' })
      .eq('id', existingOrder.id)
      .select();

    const order = (updatedOrders && updatedOrders[0]) || existingOrder;

    // 3. Find closest available rider
    const assignedRider = await findBestAvailableRider(order.pickup_address);

    if (assignedRider) {
      await supabase.from('orders').update({ rider_id: assignedRider.id }).eq('id', order.id);
      await supabase.from('riders').update({ status: 'busy' }).eq('id', assignedRider.id);

      console.log(`[Dispatch] Rider ${assignedRider.name} assigned to order ${order.paystack_reference}`);

      // Notify Customer on WhatsApp
      const customerMsg = `✅ *Payment Confirmed!* 🎉\n\n` +
        `Your FM XPRESS dispatch order *${order.paystack_reference}* is active.\n\n` +
        `🏍️ *Dispatched Rider:* ${assignedRider.name}\n` +
        `📞 *Rider Contact:* +${assignedRider.phone_number}\n` +
        `📍 *Pickup Address:* ${order.pickup_address}\n` +
        `🏁 *Delivery Address:* ${order.delivery_address}\n\n` +
        `Your rider is heading to the pickup location now! 🚀`;

      await sendWhatsAppMessage(order.customer_phone, customerMsg);

      // Notify Rider on WhatsApp
      const riderMsg = `🔔 *NEW DISPATCH ASSIGNMENT - FM XPRESS*\n\n` +
        `🆔 *Order Ref:* ${order.paystack_reference}\n` +
        `📍 *Pickup:* ${order.pickup_address}\n` +
        `🏁 *Delivery:* ${order.delivery_address}\n` +
        `📏 *Distance:* ${order.distance_km} km\n` +
        `📦 *Package:* ${(order.package_size || 'STANDARD').toUpperCase()}\n` +
        `👤 *Customer Phone:* +${order.customer_phone}\n\n` +
        `👉 *Action:* When package is delivered, reply *DELIVERED* to complete this job and receive new orders!`;

      await sendWhatsAppMessage(assignedRider.phone_number, riderMsg);

      return { order, rider: assignedRider };
    } else {
      console.log(`[Dispatch] No available riders right now. Order ${order.paystack_reference} queued.`);
      const queueMsg = `✅ *Payment Confirmed!* 🎉\n\n` +
        `We have received your payment for order *${order.paystack_reference}*.\n\n` +
        `⏳ All our dispatch riders are currently on active deliveries. Your order has been placed in our priority queue! The next available rider will be assigned to you shortly.`;
      await sendWhatsAppMessage(order.customer_phone, queueMsg);

      return { order, rider: null };
    }
  } catch (err) {
    console.error("[Payment Handler Error]:", err.message);
    return null;
  }
}

// GET /payment-callback - Instant browser redirect after customer pays on Paystack
app.get('/payment-callback', async (req, res) => {
  let rawRef = req.query.reference || req.query.trxref;
  const reference = Array.isArray(rawRef) 
    ? rawRef[0] 
    : (typeof rawRef === 'string' ? rawRef.split(',')[0].trim() : rawRef);

  console.log(`[Payment Callback] Customer returned to /payment-callback with reference: ${reference}`);

  if (!reference) {
    return res.status(400).send('Missing transaction reference.');
  }

  try {
    const secretKey = (process.env.PAYSTACK_SECRET_KEY || '').trim();
    const verifyRes = await axios.get(`https://api.paystack.co/transaction/verify/${reference}`, {
      headers: { Authorization: `Bearer ${secretKey}` }
    });

    const txData = verifyRes.data && verifyRes.data.data;
    if (txData && txData.status === 'success') {
      const result = await handleSuccessfulPayment(reference, txData.amount / 100);
      const riderInfoHtml = result && result.rider 
        ? `<div class="text-left bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs space-y-1.5">
             <div class="text-slate-400 font-semibold uppercase text-[10px]">Assigned Dispatch Rider</div>
             <div class="text-white font-bold text-sm flex items-center gap-2">🏍️ ${result.rider.name}</div>
             <div class="text-slate-300">📞 +${result.rider.phone_number}</div>
           </div>`
        : `<p class="text-xs text-amber-400">Order queued! Next available rider will be assigned momentarily.</p>`;

      const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Payment Successful - FM XPRESS</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white min-h-screen flex items-center justify-center p-4 font-sans">
  <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 max-w-sm w-full text-center space-y-5 shadow-2xl">
    <div class="w-16 h-16 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-2xl flex items-center justify-center mx-auto text-3xl">
      ✓
    </div>
    <div>
      <h1 class="text-xl font-bold text-white">Payment Confirmed!</h1>
      <p class="text-xs text-slate-400 mt-1">Ref: <span class="font-mono text-slate-300">${reference}</span></p>
    </div>
    <div class="p-3.5 bg-slate-950/80 rounded-2xl border border-slate-800 text-xs text-slate-400 space-y-1.5">
      <div class="flex justify-between items-center"><span class="text-slate-500">Amount Paid:</span><span class="font-bold text-emerald-400 text-sm">₦${((txData.amount || 0) / 100).toLocaleString('en-NG')}</span></div>
      <div class="flex justify-between items-center"><span class="text-slate-500">Dispatch Status:</span><span class="text-sky-400 font-semibold">Rider Dispatched 🚀</span></div>
    </div>
    ${riderInfoHtml}
    <a href="https://wa.me/2349036869830" class="block w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-bold text-sm transition shadow-lg">
      Return to WhatsApp
    </a>
    <p class="text-[11px] text-slate-500">We have sent full rider and tracking details directly to your WhatsApp!</p>
  </div>
</body>
</html>`;

      return res.send(html);
    } else {
      return res.status(400).send(`Payment verification status: ${txData ? txData.status : 'unknown'}`);
    }
  } catch (err) {
    console.error("[Payment Callback Error]:", err.response ? err.response.data : err.message);
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Payment Status - FM XPRESS</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white min-h-screen flex items-center justify-center p-4 font-sans">
  <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 max-w-sm w-full text-center space-y-4 shadow-2xl">
    <div class="w-14 h-14 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-2xl flex items-center justify-center mx-auto text-2xl">
      ⚠️
    </div>
    <h1 class="text-lg font-bold text-white">Payment Processing</h1>
    <p class="text-xs text-slate-400">Reference: <span class="font-mono text-slate-300">${reference}</span></p>
    <p class="text-xs text-slate-300">If your payment went through, our automated dispatcher will notify you and assign your rider on WhatsApp in a moment.</p>
    <a href="https://wa.me/2349036869830" class="block w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-bold text-xs transition shadow-lg">
      Return to WhatsApp
    </a>
  </div>
</body>
</html>`;
    return res.status(200).send(html);
  }
});

// POST /paystack-webhook - Asynchronous webhook confirmation from Paystack
app.post('/paystack-webhook', async (req, res) => {
  res.sendStatus(200);
  const event = req.body;
  if (event && event.event === 'charge.success') {
    const reference = event.data.reference;
    await handleSuccessfulPayment(reference, event.data.amount / 100);
  }
});

// --- Core Order Processing & Paystack Payment Generation ---
async function processOrderAndSendPayment(from, pickup, delivery, size = 'medium', precomputedDistanceKm = null, extraDetails = null) {
  // 1. Check if an available rider exists and evaluate proximity
  const bestRider = await findBestAvailableRider(pickup);
  
  if (!bestRider) {
    console.log(`[Riders] No riders available for order from ${from}`);
    await sendWhatsAppMessage(from, "⚠️ Sorry, all FM XPRESS riders are currently busy! Please try again in 15 minutes.");
    return;
  }

  const settings = getPricingSettings();
  const maxPickupRadius = settings.max_pickup_distance_km || 7;
  let farPickupSurcharge = 0;

  // Far-Rider Restriction Check
  if (bestRider.distanceToPickupKm > maxPickupRadius) {
    if (settings.allow_far_pickup_with_surcharge) {
      farPickupSurcharge = settings.far_pickup_surcharge || 800;
      console.log(`[Proximity Alert] Closest rider (${bestRider.name} in ${bestRider.current_zone}) is ${bestRider.distanceToPickupKm} km away. Adding ₦${farPickupSurcharge} far-pickup fuel surcharge.`);
    } else {
      // Strict Local Dispatch Mode (Mode A): Prevent far dispatch to avoid deadhead mileage loss
      await sendWhatsAppMessage(
        from,
        `⚠️ All FM XPRESS riders in your immediate area are currently on active deliveries. The nearest rider is in *${bestRider.current_zone}* (${bestRider.distanceToPickupKm} km away).\n\nTo prevent dispatch delays and keep fares low, please check back in 15–20 minutes when a local rider finishes their delivery!\n\n_(Reply MENU to return to main options)_`
      );
      return;
    }
  }
  
  let distanceKm = precomputedDistanceKm;

  if (!distanceKm) {
    await sendWhatsAppMessage(from, `Calculating the fastest route from "${pickup}" to "${delivery}"... ⏳`);

    // 1. Check Google Maps first (Gold standard)
    const googleRoute = await getGoogleMapsDistance(pickup, delivery);
    if (googleRoute) {
      distanceKm = googleRoute.distanceKm;
    } else {
      // 2. Fallback to OpenRouteService + Local Knowledge Base
      const pickupRes = await getCoordinatesWithDetails(pickup);
      const deliveryRes = await getCoordinatesWithDetails(delivery);

      if (pickupRes && deliveryRes) {
        const distanceMeters = await getDrivingDistance(pickupRes.coords, deliveryRes.coords);
        if (!distanceMeters) {
          await sendWhatsAppMessage(from, "⚠️ We could not find a drivable road route between those two locations. Please provide more specific street addresses or landmarks.");
          return;
        }
        distanceKm = (distanceMeters / 1000).toFixed(1);
      } else {
        console.warn(`[Routing] Geocoding failed for one of: "${pickup}" or "${delivery}"`);
        await sendWhatsAppMessage(from, `⚠️ We couldn't locate one of those addresses. Please verify the locations or landmarks.`);
        return;
      }
    }
  }

  // Dynamic Pricing: Base fee + (distance * rate) + Far-pickup surcharge (if applicable)
  const price = settings.base_fee + (Number(distanceKm) * settings.per_km_rate) + farPickupSurcharge;
  console.log(`[Pricing] Route: ${distanceKm} km (Base: ₦${settings.base_fee}, Rate: ₦${settings.per_km_rate}/km, Surcharge: ₦${farPickupSurcharge}). Calculated Price: ₦${price}`);
  
  // Generate a unique reference for Paystack
  const paystackRef = 'FMX_' + Date.now();
  
  // Combine recipient details into delivery address if provided
  let finalDeliveryAddress = delivery;
  if (extraDetails && extraDetails.recipient_info) {
    finalDeliveryAddress = `${delivery} [Recipient: ${extraDetails.recipient_info}]`;
  } else if (extraDetails && extraDetails.recipient_name) {
    finalDeliveryAddress = `${delivery} [Recipient: ${extraDetails.recipient_name} ${extraDetails.recipient_phone || ''}]`;
  }

  // Save the pending order to Supabase
  const { error } = await supabase
    .from('orders')
    .insert([
      { 
        customer_phone: from, 
        pickup_address: pickup, 
        delivery_address: finalDeliveryAddress, 
        package_size: size,
        distance_km: parseFloat(distanceKm),
        price_ngn: price,
        status: 'pending_payment',
        paystack_reference: paystackRef
      }
    ]);
  
  if (error) {
    console.error("[Database] Error inserting order:", error.message);
    await sendWhatsAppMessage(from, "Sorry, an internal database error occurred. Please try again.");
  } else {
    console.log(`[Database] Pending order saved for ${from} (Ref: ${paystackRef})`);
    
    // Generate the Payment Link with public callback
    const paymentLink = await generatePaystackLink(price, `customer_${from}@fmxpress.com`, paystackRef);
    
    if (paymentLink) {
       const formattedPrice = price.toLocaleString('en-NG');
       console.log(`[Paystack] Payment link generated: ${paymentLink}`);
       
       let summaryText = `📦 *FM XPRESS Delivery Booking Confirmed!*\n\n` +
         `📍 *Pickup:* ${pickup}\n` +
         `🏁 *Delivery:* ${delivery}\n` +
         `🛣️ *Distance:* ${distanceKm} km\n` +
         `💰 *Total Price:* ₦${formattedPrice}\n`;

       if (farPickupSurcharge > 0) {
         summaryText += `⚡ *Long-Distance Pickup Surcharge:* +₦${farPickupSurcharge.toLocaleString('en-NG')} _(Nearest rider dispatched from ${bestRider.current_zone}, ${bestRider.distanceToPickupKm} km away)_\n`;
       }

       if (extraDetails && (extraDetails.recipient_info || extraDetails.recipient_name)) {
         summaryText += `👤 *Recipient:* ${extraDetails.recipient_info || extraDetails.recipient_name}\n`;
       }

       summaryText += `\n💳 *Pay now to dispatch rider:*\n${paymentLink}\n\n⚡ _Your rider will be dispatched immediately once payment is confirmed!_`;
       await sendWhatsAppMessage(from, summaryText);
    } else {
       console.error(`[Paystack] Failed to generate payment link`);
       await sendWhatsAppMessage(from, "Sorry, could not generate a Paystack payment link at this time.");
    }
  }
}

async function proceedWithPickupAddress(from, session, pickupAddress) {
  const pickupRes = await getCoordinatesWithDetails(pickupAddress);

  if (!pickupRes) {
    await sendWhatsAppMessage(from, `⚠️ We couldn't quite locate "${pickupAddress}".\n\nPlease check the spelling or provide a nearby landmark or district name (e.g. "Kubwa near Total filling station"):\n\n_(Reply CANCEL to return to main menu)_`);
    return;
  }

  const pricing = getPricingSettings();
  const bestRider = await findBestAvailableRider(pickupAddress);

  // Strict Local Dispatch Mode (Mode A): Check if closest available rider is within pickup radius
  if (bestRider && bestRider.distanceToPickupKm > (pricing.max_pickup_distance_km || 7)) {
    if (!pricing.allow_far_pickup_with_surcharge) {
      delete customerSessions[from];
      await sendWhatsAppMessage(
        from,
        `⚠️ All FM XPRESS riders in your immediate area are currently on active deliveries. The nearest rider is in *${bestRider.current_zone}* (${bestRider.distanceToPickupKm} km away).\n\nTo prevent dispatch delays and keep fares low, please check back in 15–20 minutes when a local rider finishes their delivery!\n\n_(Reply MENU to return to main options)_`
      );
      return;
    }
  }

  session.pickup_address = pickupAddress;
  session.pickup_label = pickupRes.label;
  session.pickup_coords = pickupRes.coords;
  session.stage = 'AWAITING_DELIVERY';

  await sendWhatsAppMessage(
    from,
    `✅ *Pickup Set:* ${pickupAddress}\n\n🏁 *Step 2 of 3: Delivery Location*\n_(e.g. House 4, 3rd Avenue, Gwarinpa)_`
  );
}

async function proceedWithDeliveryAddress(from, session, deliveryAddress) {
  let distanceKm = null;
  let deliveryLabel = deliveryAddress;
  let deliveryCoords = null;

  // 1. Try Google Maps first (Gold standard)
  const googleRoute = await getGoogleMapsDistance(session.pickup_address, deliveryAddress);
  if (googleRoute) {
    distanceKm = googleRoute.distanceKm;
    deliveryLabel = googleRoute.deliveryResolved || deliveryAddress;
  } else {
    // 2. Fallback to OpenRouteService + Local Abuja Knowledge Base
    const deliveryRes = await getCoordinatesWithDetails(deliveryAddress);

    if (!deliveryRes) {
      await sendWhatsAppMessage(from, `⚠️ We couldn't quite locate "${deliveryAddress}".\n\nPlease provide a nearby well-known landmark, popular junction, or check spelling:\n\n_(Reply CANCEL to return to main menu)_`);
      return;
    }

    deliveryLabel = deliveryRes.label;
    deliveryCoords = deliveryRes.coords;

    const distanceMeters = await getDrivingDistance(session.pickup_coords, deliveryRes.coords);
    if (!distanceMeters) {
      await sendWhatsAppMessage(from, `⚠️ We found both locations, but couldn't map a drivable road route between them.\n\nPlease reply with a more specific delivery address or nearby major road:`);
      return;
    }

    distanceKm = (distanceMeters / 1000).toFixed(1);
  }

  // Distance safeguard (> 70 km)
  if (Number(distanceKm) > 70) {
    await sendWhatsAppMessage(from, `⚠️ This route calculated is ${distanceKm} km (between "${session.pickup_address}" and "${deliveryLabel}").\n\nFM XPRESS handles intra-city deliveries under 70 km. If your address was matched outside the city by typo, please reply with a local street or landmark in your city:\n\n_(Reply CANCEL to start over)_`);
    return;
  }

  const pricing = getPricingSettings();
  let farSurcharge = 0;
  const bestRider = await findBestAvailableRider(session.pickup_address);
  if (bestRider && bestRider.distanceToPickupKm > (pricing.max_pickup_distance_km || 7)) {
    if (pricing.allow_far_pickup_with_surcharge) {
      farSurcharge = pricing.far_pickup_surcharge || 800;
    } else {
      delete customerSessions[from];
      await sendWhatsAppMessage(
        from,
        `⚠️ All FM XPRESS riders in your immediate area are currently on active deliveries. The nearest rider is in *${bestRider.current_zone}* (${bestRider.distanceToPickupKm} km away).\n\nTo prevent dispatch delays and keep fares low, please check back in 15–20 minutes when a local rider finishes their delivery!\n\n_(Reply MENU to return to main options)_`
      );
      return;
    }
  }
  const price = pricing.base_fee + (Number(distanceKm) * pricing.per_km_rate) + farSurcharge;

  session.delivery_address = deliveryAddress;
  session.delivery_label = deliveryLabel;
  session.delivery_coords = deliveryCoords;
  session.distanceKm = distanceKm;
  session.price = price;
  session.farSurcharge = farSurcharge;
  session.stage = 'AWAITING_RECIPIENT';

  let recipientPrompt = `📦 *Route Details:*\n` +
    `📍 *Pickup:* ${session.pickup_address}\n` +
    `🏁 *Delivery:* ${deliveryAddress}\n` +
    `🛣️ *Distance:* ${distanceKm} km\n`;

  if (farSurcharge > 0) {
    recipientPrompt += `⚡ *Long-Distance Surcharge:* +₦${farSurcharge.toLocaleString('en-NG')} _(Nearest rider in ${bestRider.current_zone})_\n`;
  }

  recipientPrompt += `💰 *Estimated Price:* ₦${price.toLocaleString('en-NG')}\n\n` +
    `👤 *Step 3 of 3: Recipient*\n` +
    `_(e.g. Amina Bello, 08012345678)_`;

  await sendWhatsAppMessage(from, recipientPrompt);
}

// 3. Webhook endpoint to receive incoming WhatsApp messages
app.post('/webhook', async (req, res) => {
  const body = req.body;

  if (body.object === 'whatsapp_business_account') {
    res.status(200).send('EVENT_RECEIVED');
    
    // Loop through the entries (messages)
    for (const entry of body.entry) {
      const changes = entry.changes[0];
      const value = changes.value;

      if (value.messages && value.messages[0]) {
        const message = value.messages[0];
        const from = message.from; 

        console.log(`[WhatsApp] Incoming message from ${from}, type: ${message.type}`);

        // A. Handle WhatsApp Interactive replies (List Selection & Buttons)
        if (message.type === 'interactive') {
          const interactive = message.interactive;

          // List item tapped
          if (interactive.type === 'list_reply') {
            const selectedId = interactive.list_reply.id;
            console.log(`[WhatsApp List Reply] from ${from}: ${selectedId}`);

            if (selectedId === 'menu_send_package') {
              await handleSendPackage(from);
              return;
            }
            if (selectedId === 'menu_track_order') {
              await handleTrackOrder(from);
              return;
            }
            if (selectedId === 'menu_get_price') {
              await handleGetPrice(from);
              return;
            }
            if (selectedId === 'menu_support') {
              await handleSupport(from);
              return;
            }
          }

          // Reply button tapped
          if (interactive.type === 'button_reply') {
            const btnId = interactive.button_reply.id;
            console.log(`[WhatsApp Button Reply] from ${from}: ${btnId}`);

            if (btnId === 'btn_send_package' || btnId === 'menu_send_package') {
              delete customerSessions[from];
              await handleSendPackage(from);
              return;
            }

            if (btnId === 'btn_track_order' || btnId === 'menu_track_order') {
              delete customerSessions[from];
              await handleTrackOrder(from);
              return;
            }

            if (btnId === 'btn_support' || btnId === 'menu_support') {
              delete customerSessions[from];
              await handleSupport(from);
              return;
            }

            if (btnId === 'btn_accept_pickup_sugg') {
              const session = customerSessions[from];
              if (session && session.stage === 'CONFIRM_PICKUP_SUGGESTION') {
                const addr = session.pending_pickup_suggestion;
                delete session.pending_pickup_suggestion;
                delete session.pending_pickup_raw;
                await proceedWithPickupAddress(from, session, addr);
                return;
              }
            }

            if (btnId === 'btn_keep_pickup_raw') {
              const session = customerSessions[from];
              if (session && session.stage === 'CONFIRM_PICKUP_SUGGESTION') {
                const addr = session.pending_pickup_raw;
                delete session.pending_pickup_suggestion;
                delete session.pending_pickup_raw;
                await proceedWithPickupAddress(from, session, addr);
                return;
              }
            }

            if (btnId === 'btn_accept_deliv_sugg') {
              const session = customerSessions[from];
              if (session && session.stage === 'CONFIRM_DELIVERY_SUGGESTION') {
                const addr = session.pending_delivery_suggestion;
                delete session.pending_delivery_suggestion;
                delete session.pending_delivery_raw;
                await proceedWithDeliveryAddress(from, session, addr);
                return;
              }
            }

            if (btnId === 'btn_keep_deliv_raw') {
              const session = customerSessions[from];
              if (session && session.stage === 'CONFIRM_DELIVERY_SUGGESTION') {
                const addr = session.pending_delivery_raw;
                delete session.pending_delivery_suggestion;
                delete session.pending_delivery_raw;
                await proceedWithDeliveryAddress(from, session, addr);
                return;
              }
            }

            if (btnId === 'btn_confirm_order') {
              const session = customerSessions[from];
              if (session && session.stage === 'CONFIRM_ORDER') {
                delete customerSessions[from];
                await processOrderAndSendPayment(
                  from,
                  session.pickup_address,
                  session.delivery_address,
                  session.package_size || 'medium',
                  session.distanceKm,
                  { recipient_info: session.recipient_info }
                );
                return;
              }
            }

            if (btnId === 'btn_cancel_order') {
              delete customerSessions[from];
              await sendWhatsAppMessage(from, "🔄 Order cancelled.");
              await sendWhatsAppInteractiveMenu(from);
              return;
            }
          }

          // WhatsApp Flow form submissions (nfm_reply)
          if (interactive.type === 'nfm_reply') {
            try {
              const flowData = JSON.parse(interactive.nfm_reply.response_json);
              const { pickup, delivery, size, sender_name, recipient_name, recipient_phone, instructions } = flowData;
              console.log(`[Flow] Form submitted by ${from}: pickup="${pickup}", delivery="${delivery}", size="${size}"`);
              delete customerSessions[from];
              await processOrderAndSendPayment(from, pickup, delivery, size || 'medium', null, {
                sender_name,
                recipient_name,
                recipient_phone,
                instructions
              });
            } catch (err) {
              console.error("[Flow Parse Error]:", err.message);
            }
            return;
          }
        }

        // B. Handle standard text messages
        if (message.type === 'text') {
          const msg_body = message.text.body.trim();
          console.log(`[WhatsApp] Text content from ${from}: "${msg_body}"`);
          
          // 1. Rider completion command: "DELIVERED" or "DONE"
          if (msg_body.toUpperCase().startsWith('DELIVERED') || msg_body.toUpperCase().startsWith('DONE')) {
            console.log(`[Rider Command] Processing delivery completion from ${from}`);
            const { data: riderMatch } = await supabase.from('riders').select('*').eq('phone_number', from);
            if (riderMatch && riderMatch.length > 0) {
              const rider = riderMatch[0];
              const { data: activeOrders } = await supabase
                .from('orders')
                .select('*')
                .eq('rider_id', rider.id)
                .eq('status', 'paid')
                .order('created_at', { ascending: false })
                .limit(1);

              if (activeOrders && activeOrders.length > 0) {
                await supabase.from('orders').update({ status: 'delivered' }).eq('id', order.id);
                await supabase.from('riders').update({ status: 'available' }).eq('id', rider.id);

                // Update rider station to delivery area
                const newZone = extractDistrictName(order.delivery_address);
                setRiderCurrentZone(rider.id, newZone);
                console.log(`[Rider Location Updated] Rider ${rider.name} is now stationed at: ${newZone}`);

                console.log(`[Rider Command] Order ${order.id} marked delivered, rider ${rider.name} available`);

                await sendWhatsAppMessage(from, `✅ Fantastic job, ${rider.name}! Order ${order.paystack_reference} is marked as *DELIVERED*.\n\nYour status is reset to *AVAILABLE* at *${newZone}* for new delivery jobs.`);
                await sendWhatsAppMessage(order.customer_phone, `🎉 *Delivery Complete!*\n\nYour package has been successfully delivered by ${rider.name}.\n\nThank you for choosing *FM XPRESS*! 🚚`);
              } else {
                await sendWhatsAppMessage(from, `You don't have any active delivery assigned right now.`);
              }
            } else {
              await sendWhatsAppMessage(from, `This number is not registered as an active FM XPRESS rider.`);
            }
            return;
          }

          // 2. Customer cancel / reset / menu commands
          if (['CANCEL', 'RESET', 'MENU', 'START'].includes(msg_body.toUpperCase())) {
            delete customerSessions[from];
            if (msg_body.toUpperCase() === 'CANCEL' || msg_body.toUpperCase() === 'RESET') {
              await sendWhatsAppMessage(from, "🔄 Session reset.");
            }
            await sendWhatsAppInteractiveMenu(from);
            return;
          }

          // 3. Quick direct menu option matching: "1", "2", "3", "4", "send", "track", "price", "support"
          const matchedMenu = matchMenuOption(msg_body);
          if (matchedMenu) {
            delete customerSessions[from];
            if (matchedMenu === 'menu_send_package') {
              await handleSendPackage(from);
              return;
            }
            if (matchedMenu === 'menu_track_order') {
              await handleTrackOrder(from);
              return;
            }
            if (matchedMenu === 'menu_get_price') {
              await handleGetPrice(from);
              return;
            }
            if (matchedMenu === 'menu_support') {
              await handleSupport(from);
              return;
            }
          }

          // 4. Quick shortcut: "From: ... To: ..." (one message)
          const fromMatch = msg_body.match(/from:\s*([^\n\r,]+(?:,[^\n\r]+)*?)(?=\s*to:|$)/i);
          const toMatch = msg_body.match(/to:\s*([^\n\r,]+(?:,[^\n\r]+)*)/i);

          if (fromMatch && toMatch) {
            delete customerSessions[from];
            const pickup = fromMatch[1].trim();
            const delivery = toMatch[1].trim();
            console.log(`[WhatsApp] Extracted text addresses: Pickup="${pickup}", Delivery="${delivery}"`);
            await processOrderAndSendPayment(from, pickup, delivery, 'medium');
            return;
          }

          // 5. Active Multi-step conversational flow
          const session = customerSessions[from];

          // STAGE 4: Confirmation
          if (session && session.stage === 'CONFIRM_ORDER') {
            if (['CONFIRM', 'YES', 'OK', 'PAY', 'PROCEED'].includes(msg_body.toUpperCase())) {
              delete customerSessions[from];
              await processOrderAndSendPayment(
                from,
                session.pickup_address,
                session.delivery_address,
                session.package_size || 'medium',
                session.distanceKm,
                { recipient_info: session.recipient_info }
              );
              return;
            } else {
              await sendWhatsAppButtons(
                from,
                `📋 Please confirm your delivery:\n\n📍 *Pickup:* ${session.pickup_address}\n🏁 *Delivery:* ${session.delivery_address}\n👤 *Recipient:* ${session.recipient_info}\n🛣️ *Distance:* ${session.distanceKm} km\n💰 *Total Price:* ₦${session.price.toLocaleString('en-NG')}`,
                [
                  { id: 'btn_confirm_order', title: 'Confirm Delivery' },
                  { id: 'btn_cancel_order', title: 'Cancel' }
                ]
              );
              return;
            }
          }

          // STAGE 3: Waiting for Recipient Details
          if (session && session.stage === 'AWAITING_RECIPIENT') {
            session.recipient_info = msg_body;
            session.stage = 'CONFIRM_ORDER';

            const summaryBody = `📋 *Order Summary*\n\n` +
              `📍 *Pickup:* ${session.pickup_address}\n` +
              `🏁 *Delivery:* ${session.delivery_address}\n` +
              `👤 *Recipient:* ${session.recipient_info}\n` +
              `🛣️ *Distance:* ${session.distanceKm} km\n` +
              `💰 *Total Price:* ₦${session.price.toLocaleString('en-NG')}\n\n` +
              `Tap *Confirm Delivery* to get your payment link:`;

            await sendWhatsAppButtons(from, summaryBody, [
              { id: 'btn_confirm_order', title: 'Confirm Delivery' },
              { id: 'btn_cancel_order', title: 'Cancel' }
            ]);
            return;
          }

          // STAGE 2.5: User reviewing Delivery Address Suggestion
          if (session && session.stage === 'CONFIRM_DELIVERY_SUGGESTION') {
            const upper = msg_body.toUpperCase().trim();
            if (['YES', '1', 'OK', 'CONFIRM', 'USE THIS', 'CORRECT'].includes(upper)) {
              const addr = session.pending_delivery_suggestion;
              delete session.pending_delivery_suggestion;
              delete session.pending_delivery_raw;
              await proceedWithDeliveryAddress(from, session, addr);
              return;
            } else if (['KEEP', 'RAW', '2', 'NO', 'MINE'].includes(upper)) {
              const addr = session.pending_delivery_raw;
              delete session.pending_delivery_suggestion;
              delete session.pending_delivery_raw;
              await proceedWithDeliveryAddress(from, session, addr);
              return;
            } else {
              delete session.pending_delivery_suggestion;
              delete session.pending_delivery_raw;
              session.stage = 'AWAITING_DELIVERY';
              // Falls through to process the new text as delivery address
            }
          }

          // STAGE 2: Waiting for Delivery Address
          if (session && session.stage === 'AWAITING_DELIVERY') {
            // Check Google Places Autocomplete for smart suggestions & typo correction
            const suggestions = await getGooglePlacesSuggestions(msg_body);
            if (suggestions && suggestions.length > 0) {
              const topMatch = suggestions[0];
              const normalizedTyped = msg_body.toLowerCase().replace(/[^a-z0-9]/g, '');
              const normalizedSugg = topMatch.description.toLowerCase().replace(/[^a-z0-9]/g, '');

              if (normalizedTyped !== normalizedSugg) {
                session.pending_delivery_suggestion = topMatch.description;
                session.pending_delivery_raw = msg_body;
                session.stage = 'CONFIRM_DELIVERY_SUGGESTION';

                await sendWhatsAppButtons(
                  from,
                  `🏁 *Location Match*\n\nDid you mean:\n👉 *${topMatch.description}*?`,
                  [
                    { id: 'btn_accept_deliv_sugg', title: 'Yes, Use This ✅' },
                    { id: 'btn_keep_deliv_raw', title: 'Keep What I Typed' }
                  ]
                );
                return;
              }
            }

            await proceedWithDeliveryAddress(from, session, msg_body);
            return;
          }

          // STAGE 1.5: User reviewing Pickup Address Suggestion
          if (session && session.stage === 'CONFIRM_PICKUP_SUGGESTION') {
            const upper = msg_body.toUpperCase().trim();
            if (['YES', '1', 'OK', 'CONFIRM', 'USE THIS', 'CORRECT'].includes(upper)) {
              const addr = session.pending_pickup_suggestion;
              delete session.pending_pickup_suggestion;
              delete session.pending_pickup_raw;
              await proceedWithPickupAddress(from, session, addr);
              return;
            } else if (['KEEP', 'RAW', '2', 'NO', 'MINE'].includes(upper)) {
              const addr = session.pending_pickup_raw;
              delete session.pending_pickup_suggestion;
              delete session.pending_pickup_raw;
              await proceedWithPickupAddress(from, session, addr);
              return;
            } else {
              delete session.pending_pickup_suggestion;
              delete session.pending_pickup_raw;
              session.stage = 'AWAITING_PICKUP';
              // Falls through to process the new text as pickup address
            }
          }

          // STAGE 1: Waiting for Pickup Address
          if (session && session.stage === 'AWAITING_PICKUP') {
            // Check Google Places Autocomplete for smart suggestions & typo correction
            const suggestions = await getGooglePlacesSuggestions(msg_body);
            if (suggestions && suggestions.length > 0) {
              const topMatch = suggestions[0];
              const normalizedTyped = msg_body.toLowerCase().replace(/[^a-z0-9]/g, '');
              const normalizedSugg = topMatch.description.toLowerCase().replace(/[^a-z0-9]/g, '');

              if (normalizedTyped !== normalizedSugg) {
                session.pending_pickup_suggestion = topMatch.description;
                session.pending_pickup_raw = msg_body;
                session.stage = 'CONFIRM_PICKUP_SUGGESTION';

                await sendWhatsAppButtons(
                  from,
                  `📍 *Location Match*\n\nDid you mean:\n👉 *${topMatch.description}*?`,
                  [
                    { id: 'btn_accept_pickup_sugg', title: 'Yes, Use This ✅' },
                    { id: 'btn_keep_pickup_raw', title: 'Keep What I Typed' }
                  ]
                );
                return;
              }
            }

            await proceedWithPickupAddress(from, session, msg_body);
            return;
          }

          // 6. DEFAULT GREETING: If no active session or greeting text received, display the 4-Option Menu!
          await sendWhatsAppInteractiveMenu(from);
        }
      }
    }
  } else {
    res.sendStatus(404);
  }
});

async function sendWhatsAppMessage(to, text) {
  try {
    const res = await axios.post(`https://graph.facebook.com/v17.0/${process.env.PHONE_NUMBER_ID}/messages`, {
      messaging_product: "whatsapp",
      to: to,
      text: { body: text }
    }, {
      headers: {
        "Authorization": `Bearer ${process.env.WHATSAPP_TOKEN}`,
        "Content-Type": "application/json"
      }
    });
    console.log(`[WhatsApp] Message successfully sent to ${to}: ID ${res.data.messages[0].id}`);
  } catch (error) {
    console.error("[WhatsApp] Error sending message:", error.response ? error.response.data : error.message);
  }
}

// --- Start Server ---
if (!process.env.VERCEL) {
  app.listen(PORT, () => {
    console.log(`FM XPRESS Live Dispatch Server listening on port ${PORT}`);
  });
}

module.exports = app;
