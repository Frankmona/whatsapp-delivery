#!/usr/bin/env python3
import base64
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')

# Load Courier Photo as Base64 for Self-Contained SVG
courier_photo_path = os.path.join(ASSETS_DIR, 'fmxpress_courier_photo.jpg')
with open(courier_photo_path, 'rb') as f:
    courier_b64 = base64.b64encode(f.read()).decode('utf-8')

# Read QR Code path data from whatsapp_qr.svg
qr_svg_path = os.path.join(ASSETS_DIR, 'whatsapp_qr.svg')
with open(qr_svg_path, 'r') as f:
    qr_content = f.read()

# Extract the actual path 'd' attribute from whatsapp_qr.svg
import re
d_match = re.search(r'\sd="(M[^"]+)"', qr_content)
qr_path_d = d_match.group(1) if d_match else ""

# -------------------------------------------------------------
# 1. FRONT FLYER SVG (1819 x 2551 px = 154 x 216 mm @ 300 DPI)
# -------------------------------------------------------------
front_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1819" height="2551" viewBox="0 0 1819 2551">
  <defs>
    <linearGradient id="bgGradFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="45%" stop-color="#0B0F19" />
      <stop offset="100%" stop-color="#051E16" />
    </linearGradient>

    <linearGradient id="emeraldPill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>

    <linearGradient id="ctaCardGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#14B8A6" />
    </linearGradient>

    <radialGradient id="glowG" cx="80%" cy="10%" r="50%">
      <stop offset="0%" stop-color="#10B981" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#10B981" stop-opacity="0" />
    </radialGradient>

    <clipPath id="heroClip">
      <rect x="105" y="670" width="1609" height="690" rx="40" ry="40" />
    </clipPath>
  </defs>

  <!-- Full Bleed Background -->
  <rect width="1819" height="2551" fill="url(#bgGradFront)" />
  <circle cx="1500" cy="300" r="600" fill="url(#glowG)" />
  <circle cx="200" cy="2200" r="500" fill="url(#glowG)" />

  <!-- Crop Marks at Trim Line (148 x 210 mm, 3mm = 35px from edges) -->
  <g stroke="#94A3B8" stroke-width="2" opacity="0.6">
    <!-- Top-Left -->
    <line x1="35" y1="0" x2="35" y2="25" />
    <line x1="0" y1="35" x2="25" y2="35" />
    <!-- Top-Right -->
    <line x1="1784" y1="0" x2="1784" y2="25" />
    <line x1="1794" y1="35" x2="1819" y2="35" />
    <!-- Bottom-Left -->
    <line x1="35" y1="2526" x2="35" y2="2551" />
    <line x1="0" y1="2516" x2="25" y2="2516" />
    <!-- Bottom-Right -->
    <line x1="1784" y1="2526" x2="1784" y2="2551" />
    <line x1="1794" y1="2516" x2="1819" y2="2516" />
  </g>

  <!-- SAFE AREA CONTENT CONTAINER (Centered within 35px bleed) -->
  <g transform="translate(0, 0)">

    <!-- ==================== 1. TOP HEADER ==================== -->
    <g transform="translate(105, 120)">
      <!-- Squircle Bike Icon Badge -->
      <rect x="0" y="0" width="110" height="110" rx="30" fill="url(#emeraldPill)" />
      <g transform="translate(20, 20)">
        <!-- Courier Bike Silhouette -->
        <circle cx="20" cy="50" r="12" fill="#0B1329" stroke="#FFFFFF" stroke-width="3"/>
        <circle cx="50" cy="50" r="12" fill="#0B1329" stroke="#FFFFFF" stroke-width="3"/>
        <path d="M 20 50 L 32 40 L 42 40 L 50 50 L 46 38 L 34 38 Z" fill="#FFFFFF"/>
        <rect x="14" y="28" width="14" height="14" rx="3" fill="#FFFFFF"/>
        <circle cx="44" cy="24" r="6" fill="#0B1329"/>
      </g>

      <!-- Brand Typography -->
      <text x="130" y="65" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="58" letter-spacing="-1">
        <tspan fill="#FFFFFF">FM</tspan><tspan fill="#10B981"> XPRESS</tspan>
      </text>
      <text x="132" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="20" fill="#34D399" letter-spacing="4">
        DISPATCH &amp; LOGISTICS
      </text>

      <!-- Speed Badge Right -->
      <rect x="1139" y="18" width="470" height="74" rx="37" fill="#10B981" fill-opacity="0.15" stroke="#10B981" stroke-width="2.5" />
      <circle cx="1180" cy="55" r="9" fill="#10B981" />
      <text x="1205" y="62" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="22" fill="#6EE7B7" letter-spacing="2">
        ABUJA'S FASTEST DISPATCH
      </text>
    </g>

    <line x1="105" y1="270" x2="1714" y2="270" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="2" />

    <!-- ==================== 2. HERO HEADLINE ==================== -->
    <g transform="translate(909, 360)" text-anchor="middle">
      <!-- 30-Min Rapid Pickup Tag -->
      <rect x="-240" y="-35" width="480" height="52" rx="14" fill="#F59E0B" fill-opacity="0.15" stroke="#F59E0B" stroke-opacity="0.4" stroke-width="2"/>
      <text y="0" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="23" fill="#FCD34D" letter-spacing="2">
        ⚡ 30-MINUTE RAPID DOORSTEP PICKUP
      </text>

      <!-- Main Headline -->
      <text y="90" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="70" fill="#FFFFFF" letter-spacing="-1">
        FAST, RELIABLE &amp; ON-TIME
      </text>
      <text y="170" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="70" fill="#34D399" letter-spacing="-1">
        DELIVERY ACROSS ABUJA
      </text>
      <text y="240" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="27" fill="#CBD5E1">
        From emergency documents &amp; e-commerce parcels to boutique fashion &amp; food drops
      </text>
    </g>

    <!-- ==================== 3. COURIER HERO IMAGE ==================== -->
    <g clip-path="url(#heroClip)">
      <image href="data:image/jpeg;base64,{courier_b64}" x="105" y="670" width="1609" height="690" preserveAspectRatio="xMidYMid slice" />
      <!-- Subtle Dark Gradient at bottom of photo -->
      <rect x="105" y="1170" width="1609" height="190" fill="url(#bgGradFront)" opacity="0.85" />
    </g>
    <!-- Photo Border -->
    <rect x="105" y="670" width="1609" height="690" rx="40" ry="40" fill="none" stroke="#10B981" stroke-width="4" stroke-opacity="0.4"/>
    
    <!-- Badges Overlaid on Photo -->
    <g transform="translate(150, 1290)">
      <rect x="0" y="0" width="480" height="52" rx="16" fill="#0B0F19" fill-opacity="0.92" stroke="#10B981" stroke-width="2"/>
      <text x="25" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="700" font-size="21" fill="#A7F3D0">
        🛡️ Insulated &amp; Rainproof Boxes
      </text>
    </g>
    <g transform="translate(1250, 1290)">
      <rect x="0" y="0" width="420" height="52" rx="16" fill="#10B981" />
      <text x="35" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="20" fill="#0B0F19" letter-spacing="1">
        LIVE WHATSAPP TRACKING
      </text>
    </g>

    <!-- ==================== 4. KEY SERVICES PILLARS ==================== -->
    <g transform="translate(105, 1400)">
      <!-- Col 1 -->
      <g transform="translate(0, 0)">
        <rect width="380" height="140" rx="24" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
        <circle cx="55" cy="55" r="28" fill="#10B981" fill-opacity="0.2"/>
        <text x="44" y="65" font-size="26">⚡</text>
        <text x="105" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="26" fill="#FFFFFF">Express Same-Day</text>
        <text x="105" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="19" fill="#94A3B8">Instant pickup &amp; direct drop</text>
      </g>

      <!-- Col 2 -->
      <g transform="translate(410, 0)">
        <rect width="380" height="140" rx="24" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
        <circle cx="55" cy="55" r="28" fill="#38BDF8" fill-opacity="0.2"/>
        <text x="44" y="65" font-size="26">📦</text>
        <text x="105" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="26" fill="#FFFFFF">E-Commerce Drop</text>
        <text x="105" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="19" fill="#94A3B8">Vendors &amp; boutique parcels</text>
      </g>

      <!-- Col 3 -->
      <g transform="translate(820, 0)">
        <rect width="380" height="140" rx="24" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
        <circle cx="55" cy="55" r="28" fill="#F59E0B" fill-opacity="0.2"/>
        <text x="44" y="65" font-size="26">📄</text>
        <text x="105" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="26" fill="#FFFFFF">Urgent Documents</text>
        <text x="105" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="19" fill="#94A3B8">Contracts &amp; legal files</text>
      </g>

      <!-- Col 4 -->
      <g transform="translate(1230, 0)">
        <rect width="380" height="140" rx="24" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
        <circle cx="55" cy="55" r="28" fill="#A855F7" fill-opacity="0.2"/>
        <text x="44" y="65" font-size="26">🍲</text>
        <text x="105" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="26" fill="#FFFFFF">Food &amp; Cakes</text>
        <text x="105" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="19" fill="#94A3B8">Careful upright handling</text>
      </g>
    </g>

    <!-- ==================== 5. CONVERSION CALL TO ACTION: WHATSAPP CARD ==================== -->
    <g transform="translate(105, 1580)">
      <!-- Main Green Gradient Card -->
      <rect width="1609" height="660" rx="44" fill="url(#ctaCardGrad)" />

      <!-- Left White QR Code Container -->
      <g transform="translate(70, 70)">
        <rect width="520" height="520" rx="36" fill="#FFFFFF" />
        <!-- Render Pure Vector QR Code inside container (scaled from 1000 to 440) -->
        <g transform="translate(40, 40) scale(0.44)">
          <path fill="#0F172A" d="{qr_path_d}" />
        </g>
      </g>

      <!-- Right Text & Phone Actions -->
      <g transform="translate(640, 110)">
        <!-- Badge -->
        <rect width="360" height="50" rx="25" fill="#0B0F19" />
        <text x="35" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="20" fill="#34D399" letter-spacing="1.5">
          💬 BOOK IN 60 SECONDS
        </text>

        <!-- Main Heading -->
        <text x="0" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="62" fill="#0B0F19" letter-spacing="-1">
          Scan QR or Chat On WhatsApp
        </text>
        <text x="0" y="185" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="700" font-size="30" fill="#064E3B">
          Instant transparent distance pricing &amp; immediate rider dispatch.
        </text>

        <!-- WhatsApp Phone Badge -->
        <g transform="translate(0, 230)">
          <rect width="680" height="110" rx="28" fill="#0B0F19" />
          <circle cx="65" cy="55" r="28" fill="#10B981" />
          <text x="50" y="65" font-size="28">💬</text>
          <text x="115" y="70" font-family="'Space Grotesk', -apple-system, monospace" font-weight="900" font-size="48" fill="#FFFFFF" letter-spacing="2">
            0903 686 9830
          </text>
        </g>

        <!-- Direct instructions -->
        <text x="0" y="405" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="700" font-size="24" fill="#064E3B">
          👉 Simply send "Hi" or your pickup and delivery address to start!
        </text>
      </g>
    </g>

    <!-- ==================== 6. BOTTOM CONTACT HELPLINES ==================== -->
    <g transform="translate(105, 2330)">
      <line x1="0" y1="0" x2="1609" y2="0" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="2" />
      
      <g transform="translate(0, 60)">
        <text font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-size="24" fill="#94A3B8">
          <tspan font-weight="800" fill="#10B981">📞 Admin Helpline:</tspan> <tspan font-weight="900" fill="#FFFFFF">0703 785 8093</tspan>
          <tspan dx="40" fill="#475569">|</tspan>
          <tspan dx="40" font-weight="800" fill="#F59E0B">📞 Owner / Desk:</tspan> <tspan font-weight="900" fill="#FFFFFF">0906 795 7295</tspan>
        </text>
      </g>

      <g transform="translate(1609, 60)" text-anchor="end">
        <text font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="24" fill="#34D399">
          fmxpress.tekvolutionhq.com
        </text>
      </g>
    </g>

  </g>
</svg>
'''

with open(os.path.join(SCRIPT_DIR, 'fmxpress_flyer_a5_front.svg'), 'w') as f:
    f.write(front_svg)
print("Saved Front Flyer SVG!")

# -------------------------------------------------------------
# 2. BACK FLYER SVG (1819 x 2551 px = 154 x 216 mm @ 300 DPI)
# -------------------------------------------------------------
back_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1819" height="2551" viewBox="0 0 1819 2551">
  <defs>
    <linearGradient id="bgGradBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="50%" stop-color="#0B0F19" />
      <stop offset="100%" stop-color="#061812" />
    </linearGradient>

    <linearGradient id="emeraldBanner" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669" />
      <stop offset="100%" stop-color="#10B981" />
    </linearGradient>

    <radialGradient id="glowBack" cx="20%" cy="80%" r="50%">
      <stop offset="0%" stop-color="#10B981" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#10B981" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Full Bleed Background -->
  <rect width="1819" height="2551" fill="url(#bgGradBack)" />
  <circle cx="200" cy="2000" r="700" fill="url(#glowBack)" />
  <circle cx="1600" cy="500" r="600" fill="url(#glowBack)" />

  <!-- Crop Marks at Trim Line (148 x 210 mm, 3mm = 35px from edges) -->
  <g stroke="#94A3B8" stroke-width="2" opacity="0.6">
    <line x1="35" y1="0" x2="35" y2="25" />
    <line x1="0" y1="35" x2="25" y2="35" />
    <line x1="1784" y1="0" x2="1784" y2="25" />
    <line x1="1794" y1="35" x2="1819" y2="35" />
    <line x1="35" y1="2526" x2="35" y2="2551" />
    <line x1="0" y1="2516" x2="25" y2="2516" />
    <line x1="1784" y1="2526" x2="1784" y2="2551" />
    <line x1="1794" y1="2516" x2="1819" y2="2516" />
  </g>

  <!-- SAFE CONTENT CONTAINER -->
  <g transform="translate(105, 120)">

    <!-- ==================== 1. TOP BRAND HEADER ==================== -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="80" height="80" rx="22" fill="#10B981" fill-opacity="0.2" stroke="#10B981" stroke-width="2"/>
      <text x="24" y="52" font-size="34">🗺️</text>
      <text x="105" y="48" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="44" fill="#FFFFFF" letter-spacing="-0.5">
        HOW DISPATCH WORKS WITH FM XPRESS
      </text>
      <text x="107" y="78" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="20" fill="#34D399" letter-spacing="3">
        SIMPLE 3-STEP WHATSAPP BOOKING • NO APP INSTALLATION REQUIRED!
      </text>
    </g>

    <line x1="0" y1="110" x2="1609" y2="110" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2" />

    <!-- ==================== 2. 3-STEP WORKFLOW CARDS ==================== -->
    <g transform="translate(0, 150)">
      <!-- Step 1 -->
      <g transform="translate(0, 0)">
        <rect width="510" height="300" rx="30" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
        <circle cx="65" cy="65" r="30" fill="#10B981" />
        <text x="56" y="75" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="30" fill="#0B0F19">1</text>
        <text x="120" y="72" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="32" fill="#FFFFFF">Send Details</text>
        <text x="40" y="140" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-size="23" fill="#CBD5E1" width="430">
          <tspan x="40" dy="0">Send "Hi" or your pickup</tspan>
          <tspan x="40" dy="36">&amp; delivery addresses to</tspan>
          <tspan x="40" dy="36" font-weight="800" fill="#34D399">0903 686 9830 on WhatsApp.</tspan>
        </text>
      </g>

      <!-- Step 2 -->
      <g transform="translate(550, 0)">
        <rect width="510" height="300" rx="30" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
        <circle cx="65" cy="65" r="30" fill="#10B981" />
        <text x="56" y="75" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="30" fill="#0B0F19">2</text>
        <text x="120" y="72" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="32" fill="#FFFFFF">Confirm &amp; Pay</text>
        <text x="40" y="140" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-size="23" fill="#CBD5E1">
          <tspan x="40" dy="0">Get an instant verified road</tspan>
          <tspan x="40" dy="36">distance price &amp; pay securely</tspan>
          <tspan x="40" dy="36" font-weight="800" fill="#34D399">via 1-tap Paystack link.</tspan>
        </text>
      </g>

      <!-- Step 3 -->
      <g transform="translate(1100, 0)">
        <rect width="510" height="300" rx="30" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
        <circle cx="65" cy="65" r="30" fill="#10B981" />
        <text x="56" y="75" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="30" fill="#0B0F19">3</text>
        <text x="120" y="72" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="32" fill="#FFFFFF">Rider Arrives</text>
        <text x="40" y="140" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-size="23" fill="#CBD5E1">
          <tspan x="40" dy="0">Nearest rider is attached.</tspan>
          <tspan x="40" dy="36">Receive rider contact &amp; live</tspan>
          <tspan x="40" dy="36" font-weight="800" fill="#34D399">delivery updates via chat!</tspan>
        </text>
      </g>
    </g>

    <!-- ==================== 3. TRANSPARENT PRICING SECTION ==================== -->
    <g transform="translate(0, 500)">
      <rect width="1609" height="340" rx="34" fill="#0F172A" stroke="#10B981" stroke-opacity="0.3" stroke-width="2"/>
      
      <!-- Section Header -->
      <g transform="translate(40, 45)">
        <text font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="32" fill="#FFFFFF" letter-spacing="1">
          🏷️ TRANSPARENT FAIR-DISTANCE PRICING (NO HIDDEN SURCHARGES)
        </text>
      </g>

      <!-- Pricing Box 1: Base Pickup -->
      <g transform="translate(40, 100)">
        <rect width="730" height="190" rx="24" fill="#0B0F19" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="2"/>
        <text x="40" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="700" font-size="22" fill="#94A3B8">
          BASE PICKUP FEE
        </text>
        <text x="40" y="130" font-family="'Space Grotesk', -apple-system, monospace" font-weight="900" font-size="64" fill="#34D399">
          ₦1,500
        </text>
        <text x="40" y="165" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="19" fill="#64748B">
          Standard doorstep pickup &amp; packaging inspection
        </text>
      </g>

      <!-- Pricing Box 2: Per KM Rate -->
      <g transform="translate(839, 100)">
        <rect width="730" height="190" rx="24" fill="#0B0F19" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="2"/>
        <text x="40" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="700" font-size="22" fill="#94A3B8">
          DISTANCE RATE (PER KM)
        </text>
        <text x="40" y="130" font-family="'Space Grotesk', -apple-system, monospace" font-weight="900" font-size="64" fill="#34D399">
          ₦200 <tspan font-size="32" fill="#94A3B8">/ km</tspan>
        </text>
        <text x="40" y="165" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="19" fill="#64748B">
          Calculated via verified OpenRoute GPS driving road routes
        </text>
      </g>
    </g>

    <!-- ==================== 4. FULL CITY COVERAGE MAP GRID ==================== -->
    <g transform="translate(0, 890)">
      <rect width="1609" height="520" rx="34" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>

      <g transform="translate(40, 55)">
        <text font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="34" fill="#FFFFFF">
          📍 FULL CITY COVERAGE ACROSS ABUJA (15+ STATIONS)
        </text>
        <text x="0" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="600" font-size="22" fill="#34D399">
          Riders stationed across strategic hubs for under-30-minute rapid arrival:
        </text>
      </g>

      <!-- District Pills (3 Columns) -->
      <g transform="translate(40, 160)" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-size="25" fill="#E2E8F0" font-weight="700">
        <!-- Col 1 -->
        <g transform="translate(0, 0)">
          <text y="0"><tspan fill="#10B981">●</tspan>  Wuse 2 &amp; Wuse 1</text>
          <text y="60"><tspan fill="#10B981">●</tspan>  Maitama</text>
          <text y="120"><tspan fill="#10B981">●</tspan>  Garki 1 &amp; Garki 2</text>
          <text y="180"><tspan fill="#10B981">●</tspan>  Central Business Dist.</text>
          <text y="240"><tspan fill="#10B981">●</tspan>  Asokoro &amp; Guzape</text>
        </g>

        <!-- Col 2 -->
        <g transform="translate(540, 0)">
          <text y="0"><tspan fill="#10B981">●</tspan>  Jabi &amp; Utako</text>
          <text y="60"><tspan fill="#10B981">●</tspan>  Gwarinpa Estate</text>
          <text y="120"><tspan fill="#10B981">●</tspan>  Life Camp &amp; Kado</text>
          <text y="180"><tspan fill="#10B981">●</tspan>  Dawaki &amp; Dutse</text>
          <text y="240"><tspan fill="#10B981">●</tspan>  Mabushi &amp; Katampe</text>
        </g>

        <!-- Col 3 -->
        <g transform="translate(1080, 0)">
          <text y="0"><tspan fill="#10B981">●</tspan>  Kubwa &amp; Dei-Dei</text>
          <text y="60"><tspan fill="#10B981">●</tspan>  Lugbe &amp; Airport Road</text>
          <text y="120"><tspan fill="#10B981">●</tspan>  Apo &amp; Lokogoma</text>
          <text y="180"><tspan fill="#10B981">●</tspan>  Galadimawa &amp; Games Village</text>
          <text y="240"><tspan fill="#10B981">●</tspan>  Mpape &amp; Bwari Axis</text>
        </g>
      </g>
    </g>

    <!-- ==================== 5. B2B VENDOR & MERCHANT SPECIAL PROGRAM ==================== -->
    <g transform="translate(0, 1460)">
      <rect width="1609" height="320" rx="34" fill="#0F172A" stroke="#F59E0B" stroke-opacity="0.4" stroke-width="2"/>
      
      <g transform="translate(50, 60)">
        <rect width="440" height="50" rx="14" fill="#F59E0B" fill-opacity="0.2" stroke="#F59E0B" stroke-width="2"/>
        <text x="25" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="22" fill="#FCD34D">
          👑 ARE YOU AN ABUJA BUSINESS OR VENDOR?
        </text>

        <text x="0" y="110" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="40" fill="#FFFFFF">
          Partner With FM Xpress For Discounted Batch Delivery
        </text>

        <text x="0" y="165" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="24" fill="#CBD5E1">
          Special bulk pricing, dedicated daily riders, and Priority Merchant Support for food kitchens,
        </text>
        <text x="0" y="200" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="500" font-size="24" fill="#CBD5E1">
          cake artists, pharmacies, boutiques &amp; online stores. Save up to 25% on weekly deliveries!
        </text>
      </g>
    </g>

    <!-- ==================== 6. CONTACTS & HELPLINES BANNER ==================== -->
    <g transform="translate(0, 1830)">
      <rect width="1609" height="380" rx="34" fill="url(#emeraldBanner)" />

      <!-- Content Inside Banner -->
      <g transform="translate(60, 60)">
        <text font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="44" fill="#0B0F19">
          Ready To Book A Delivery? We're Active Right Now!
        </text>
        <text y="45" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="700" font-size="26" fill="#064E3B">
          Reach our dispatch team immediately through any of the channels below:
        </text>

        <g transform="translate(0, 100)">
          <!-- Channel 1: WhatsApp -->
          <g transform="translate(0, 0)">
            <rect width="460" height="110" rx="24" fill="#0B0F19" />
            <text x="35" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="18" fill="#34D399">WHATSAPP BOOKING BOT</text>
            <text x="35" y="85" font-family="'Space Grotesk', -apple-system, monospace" font-weight="900" font-size="34" fill="#FFFFFF">0903 686 9830</text>
          </g>

          <!-- Channel 2: Admin Helpline -->
          <g transform="translate(510, 0)">
            <rect width="460" height="110" rx="24" fill="#0B0F19" />
            <text x="35" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="18" fill="#38BDF8">ADMIN DISPATCH HELPLINE</text>
            <text x="35" y="85" font-family="'Space Grotesk', -apple-system, monospace" font-weight="900" font-size="34" fill="#FFFFFF">0703 785 8093</text>
          </g>

          <!-- Channel 3: Owner / Direct Desk -->
          <g transform="translate(1020, 0)">
            <rect width="460" height="110" rx="24" fill="#0B0F19" />
            <text x="35" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="18" fill="#FCD34D">OWNER / MANAGEMENT DESK</text>
            <text x="35" y="85" font-family="'Space Grotesk', -apple-system, monospace" font-weight="900" font-size="34" fill="#FFFFFF">0906 795 7295</text>
          </g>
        </g>
      </g>
    </g>

    <!-- ==================== 7. CORPORATE FOOTER ==================== -->
    <g transform="translate(0, 2270)">
      <text font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-size="22" fill="#94A3B8">
        <tspan font-weight="800" fill="#FFFFFF">Operating Hours:</tspan> Monday – Saturday, 7:00 AM – 8:00 PM
        <tspan dx="30" fill="#475569">•</tspan>
        <tspan dx="30" font-weight="800" fill="#FFFFFF">Email:</tspan> support@fmxpress.com
      </text>

      <text x="1609" y="0" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="22" fill="#34D399">
        FM XPRESS DISPATCH &amp; LOGISTICS • ABUJA FCT, NIGERIA
      </text>
    </g>

  </g>
</svg>
'''

with open(os.path.join(SCRIPT_DIR, 'fmxpress_flyer_a5_back.svg'), 'w') as f:
    f.write(back_svg)
print("Saved Back Flyer SVG!")
