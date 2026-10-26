svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="400" viewBox="0 0 1400 400">
  <defs>
    <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>
  </defs>

  <!-- EMBLEM BADGE -->
  <g transform="translate(60, 70)">
    <!-- Squircle Background -->
    <rect x="0" y="0" width="260" height="260" rx="65" fill="url(#emeraldGrad)" />
    <!-- Inner Rim -->
    <rect x="6" y="6" width="248" height="248" rx="60" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.4" />

    <!-- Motion Speed Lines -->
    <path d="M 30 110 L 80 110" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.45" />
    <path d="M 18 140 L 72 140" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.8" />
    <path d="M 35 170 L 85 170" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.45" />

    <!-- Motorcycle Courier in Motion -->
    <!-- Rear Wheel -->
    <circle cx="90" cy="185" r="28" fill="#0B1329" stroke="#FFFFFF" stroke-width="7"/>
    <circle cx="90" cy="185" r="11" fill="#10B981"/>
    
    <!-- Front Wheel -->
    <circle cx="195" cy="185" r="28" fill="#0B1329" stroke="#FFFFFF" stroke-width="7"/>
    <circle cx="195" cy="185" r="11" fill="#10B981"/>

    <!-- Motorcycle Chassis -->
    <path d="M 90 185 L 126 158 L 160 158 L 195 185 L 175 148 L 135 148 Z" fill="#FFFFFF"/>
    
    <!-- Fork & Handlebars -->
    <path d="M 195 185 L 168 122 L 152 125" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <path d="M 168 122 L 182 106 L 170 104 Z" fill="#A7F3D0"/>

    <!-- Delivery Box -->
    <rect x="70" y="118" width="42" height="40" rx="8" fill="#FFFFFF" stroke="#0B1329" stroke-width="4"/>
    <path d="M 78 138 L 104 138" stroke="#10B981" stroke-width="5" stroke-linecap="round"/>

    <!-- Courier Rider Leaning Forward -->
    <path d="M 104 140 C 112 120, 128 114, 150 125 L 164 138 L 150 152 L 128 148 Z" fill="#0B1329"/>
    <path d="M 134 128 L 158 134 L 164 126" stroke="#0B1329" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <circle cx="144" cy="102" r="19" fill="#0B1329" stroke="#FFFFFF" stroke-width="3"/>
    <path d="M 148 95 C 158 97, 160 106, 158 111 L 148 109 Z" fill="#34D399"/>
  </g>

  <!-- TYPOGRAPHY - USING SEPARATE TEXT ELEMENTS WITH EXACT COORDINATES -->
  <g transform="translate(370, 215)">
    <!-- FM -->
    <text x="0" y="0" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="122" letter-spacing="-2" fill="#0F172A">FM</text>
    <!-- XPRESS -->
    <text x="210" y="0" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="122" letter-spacing="-2" fill="#10B981">XPRESS</text>

    <!-- SUBTITLE -->
    <text x="5" y="56" font-family="Helvetica, Arial, sans-serif" font-weight="800" font-size="28" letter-spacing="9" fill="#64748B">ABUJA DISPATCH &amp; LOGISTICS</text>
    
    <!-- ACCENT SPEED SLASH -->
    <path d="M 5 76 L 240 76" stroke="#10B981" stroke-width="6" stroke-linecap="round" />
  </g>
</svg>
"""

with open("scratch/logo_fixed.svg", "w") as f:
    f.write(svg)

