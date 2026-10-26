import os
import subprocess
import shutil

PUBLIC_DIR = "public/images"
BRAIN_DIR = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. HORIZONTAL LOGO - DARK VERSION (For White/Light Backgrounds) - NO ABUJA
# -------------------------------------------------------------------------
svg_horizontal_dark = """<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="380" viewBox="0 0 1240 380">
  <defs>
    <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>
  </defs>

  <!-- EMBLEM BADGE (Squircle + Courier) -->
  <g transform="translate(50, 50)">
    <rect x="0" y="0" width="280" height="280" rx="70" fill="url(#emeraldGrad)" />
    <rect x="7" y="7" width="266" height="266" rx="63" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.4" />

    <!-- Motion Speed Lines -->
    <path d="M 32 118 L 86 118" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.45" />
    <path d="M 20 150 L 78 150" stroke="#FFFFFF" stroke-width="8.5" stroke-linecap="round" opacity="0.8" />
    <path d="M 38 182 L 92 182" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.45" />

    <!-- Motorcycle Courier in Motion -->
    <!-- Rear Wheel -->
    <circle cx="98" cy="198" r="30" fill="#0B1329" stroke="#FFFFFF" stroke-width="7.5"/>
    <circle cx="98" cy="198" r="12" fill="#10B981"/>
    
    <!-- Front Wheel -->
    <circle cx="210" cy="198" r="30" fill="#0B1329" stroke="#FFFFFF" stroke-width="7.5"/>
    <circle cx="210" cy="198" r="12" fill="#10B981"/>

    <!-- Motorcycle Chassis -->
    <path d="M 98 198 L 136 170 L 172 170 L 210 198 L 188 158 L 145 158 Z" fill="#FFFFFF"/>
    
    <!-- Fork & Handlebars -->
    <path d="M 210 198 L 180 130 L 164 133" stroke="#FFFFFF" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <path d="M 180 130 L 196 112 L 182 110 Z" fill="#A7F3D0"/>

    <!-- Insulated Delivery Box on Rear Rack -->
    <rect x="76" y="126" width="46" height="44" rx="9" fill="#FFFFFF" stroke="#0B1329" stroke-width="4.5"/>
    <path d="M 85 148 L 113 148" stroke="#10B981" stroke-width="5.5" stroke-linecap="round"/>

    <!-- Courier Rider Aero Posture -->
    <path d="M 112 150 C 120 128, 138 122, 162 134 L 176 148 L 162 164 L 138 159 Z" fill="#0B1329"/>
    <path d="M 144 137 L 170 144 L 176 135" stroke="#0B1329" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <circle cx="155" cy="109" r="21" fill="#0B1329" stroke="#FFFFFF" stroke-width="3"/>
    <path d="M 160 101 C 170 103, 172 113, 170 119 L 160 117 Z" fill="#34D399"/>
  </g>

  <!-- TYPOGRAPHY - CLEAN DISPATCH & LOGISTICS (NO ABUJA) -->
  <g transform="translate(375, 202)">
    <text x="0" y="0" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="132" letter-spacing="-3" fill="#0F172A">FM</text>
    <text x="228" y="0" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="132" letter-spacing="-3" fill="#10B981">XPRESS</text>
    <text x="5" y="58" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="800" font-size="30" letter-spacing="10" fill="#475569">DISPATCH &amp; LOGISTICS</text>
    <path d="M 5 78 L 260 78" stroke="#10B981" stroke-width="6" stroke-linecap="round" />
  </g>
</svg>"""

# -------------------------------------------------------------------------
# 2. HORIZONTAL LOGO - LIGHT VERSION (For Black/Dark Backgrounds) - NO ABUJA
# -------------------------------------------------------------------------
svg_horizontal_light = svg_horizontal_dark.replace('fill="#0F172A">FM</text>', 'fill="#FFFFFF">FM</text>').replace('fill="#475569">DISPATCH', 'fill="#E2E8F0">DISPATCH')

# -------------------------------------------------------------------------
# 3. PURE STANDALONE BADGE CREST
# -------------------------------------------------------------------------
svg_badge_crest = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  <defs>
    <linearGradient id="crestGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>
  </defs>

  <g transform="translate(100, 100)">
    <rect x="0" y="0" width="600" height="600" rx="150" fill="url(#crestGrad)" />
    <rect x="15" y="15" width="570" height="570" rx="135" fill="none" stroke="#FFFFFF" stroke-width="7" opacity="0.4" />

    <!-- Speed Lines -->
    <path d="M 70 250 L 180 250" stroke="#FFFFFF" stroke-width="15" stroke-linecap="round" opacity="0.45" />
    <path d="M 45 320 L 165 320" stroke="#FFFFFF" stroke-width="18" stroke-linecap="round" opacity="0.8" />
    <path d="M 85 390 L 195 390" stroke="#FFFFFF" stroke-width="15" stroke-linecap="round" opacity="0.45" />

    <!-- Motorcycle Courier in Motion -->
    <!-- Rear Wheel -->
    <circle cx="210" cy="420" r="64" fill="#0B1329" stroke="#FFFFFF" stroke-width="16"/>
    <circle cx="210" cy="420" r="26" fill="#10B981"/>
    
    <!-- Front Wheel -->
    <circle cx="450" cy="420" r="64" fill="#0B1329" stroke="#FFFFFF" stroke-width="16"/>
    <circle cx="450" cy="420" r="26" fill="#10B981"/>

    <!-- Motorcycle Chassis -->
    <path d="M 210 420 L 290 360 L 370 360 L 450 420 L 400 335 L 310 335 Z" fill="#FFFFFF"/>
    
    <!-- Fork & Handlebars -->
    <path d="M 450 420 L 385 275 L 350 282" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <path d="M 385 275 L 420 236 L 390 232 Z" fill="#A7F3D0"/>

    <!-- Delivery Box -->
    <rect x="160" y="268" width="100" height="94" rx="20" fill="#FFFFFF" stroke="#0B1329" stroke-width="10"/>
    <path d="M 180 315 L 240 315" stroke="#10B981" stroke-width="12" stroke-linecap="round"/>

    <!-- Courier Rider Leaning Forward -->
    <path d="M 240 320 C 256 274, 296 260, 346 286 L 376 316 L 346 350 L 296 340 Z" fill="#0B1329"/>
    <path d="M 310 292 L 364 308 L 378 288" stroke="#0B1329" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <circle cx="332" cy="232" r="44" fill="#0B1329" stroke="#FFFFFF" stroke-width="6.5"/>
    <path d="M 342 216 C 364 220, 368 242, 364 254 L 342 250 Z" fill="#34D399"/>
  </g>
</svg>"""

# -------------------------------------------------------------------------
# 4. BADGE WITH FM XPRESS TEXT (Stacked Layout) - NO ABUJA
# -------------------------------------------------------------------------
svg_badge_stacked = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="850" viewBox="0 0 800 850">
  <defs>
    <linearGradient id="badgeGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>
  </defs>

  <!-- SQUIRCLE EMBLEM -->
  <g transform="translate(130, 40)">
    <rect x="0" y="0" width="540" height="540" rx="135" fill="url(#badgeGrad2)" />
    <rect x="13" y="13" width="514" height="514" rx="122" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.4" />

    <!-- Speed Lines -->
    <path d="M 60 225 L 160 225" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity="0.45" />
    <path d="M 38 288 L 148 288" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" opacity="0.8" />
    <path d="M 75 350 L 175 350" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity="0.45" />

    <!-- Motorcycle Courier in Motion -->
    <!-- Rear Wheel -->
    <circle cx="188" cy="380" r="58" fill="#0B1329" stroke="#FFFFFF" stroke-width="14"/>
    <circle cx="188" cy="380" r="23" fill="#10B981"/>
    
    <!-- Front Wheel -->
    <circle cx="405" cy="380" r="58" fill="#0B1329" stroke="#FFFFFF" stroke-width="14"/>
    <circle cx="405" cy="380" r="23" fill="#10B981"/>

    <!-- Motorcycle Chassis -->
    <path d="M 188 380 L 260 325 L 332 325 L 405 380 L 360 300 L 280 300 Z" fill="#FFFFFF"/>
    
    <!-- Fork & Handlebars -->
    <path d="M 405 380 L 345 250 L 315 254" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <path d="M 345 250 L 376 214 L 350 210 Z" fill="#A7F3D0"/>

    <!-- Delivery Box -->
    <rect x="144" y="242" width="90" height="85" rx="18" fill="#FFFFFF" stroke="#0B1329" stroke-width="9"/>
    <path d="M 162 284 L 216 284" stroke="#10B981" stroke-width="11" stroke-linecap="round"/>

    <!-- Courier Rider Leaning Forward -->
    <path d="M 216 288 C 230 248, 266 235, 312 258 L 338 285 L 312 315 L 266 306 Z" fill="#0B1329"/>
    <path d="M 278 264 L 328 278 L 340 260" stroke="#0B1329" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <circle cx="298" cy="210" r="40" fill="#0B1329" stroke="#FFFFFF" stroke-width="6"/>
    <path d="M 308 194 C 328 198, 332 218, 328 230 L 308 226 Z" fill="#34D399"/>
  </g>

  <!-- TYPOGRAPHY BELOW CREST - NO ABUJA -->
  <g transform="translate(145, 680)">
    <text x="0" y="0" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="88" letter-spacing="-2" fill="#0F172A">FM</text>
    <text x="155" y="0" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="88" letter-spacing="-2" fill="#10B981">XPRESS</text>
    <text x="2" y="44" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="800" font-size="22" letter-spacing="10" fill="#64748B">DISPATCH &amp; LOGISTICS</text>
  </g>
</svg>"""

# -------------------------------------------------------------------------
# 2b. HORIZONTAL LOGO - ALL WHITE (For Dark Backgrounds Monochromatic)
# -------------------------------------------------------------------------
svg_horizontal_all_white = svg_horizontal_dark.replace('fill="#0F172A">FM</text>', 'fill="#FFFFFF">FM</text>').replace('fill="#10B981">XPRESS</text>', 'fill="#FFFFFF">XPRESS</text>').replace('fill="#475569">DISPATCH', 'fill="#FFFFFF">DISPATCH').replace('stroke="#10B981"', 'stroke="#FFFFFF"')

manifest = [
    ("fmxpress_logo_dark", svg_horizontal_dark, 1140, 3720),
    ("fmxpress_logo_light", svg_horizontal_light, 1140, 3720),
    ("fmxpress_logo_all_white", svg_horizontal_all_white, 1140, 3720),
    ("fmxpress_badge_crest", svg_badge_crest, 2400, 2400),
    ("fmxpress_badge_stacked", svg_badge_stacked, 2550, 2400),
]

for name, svg_content, h, w in manifest:
    # 1. Save SVG in public/images
    svg_pub = os.path.join(PUBLIC_DIR, f"{name}.svg")
    with open(svg_pub, "w") as f:
        f.write(svg_content)
    
    # 2. Render 300 DPI Transparent PNG in public/images
    png_pub = os.path.join(PUBLIC_DIR, f"{name}.png")
    subprocess.run([
        "sips", "-s", "format", "png",
        "-s", "dpiHeight", "300.0",
        "-s", "dpiWidth", "300.0",
        "-z", str(h), str(w),
        svg_pub, "--out", png_pub
    ], check=True)
    print(f"Generated: {png_pub} ({w}x{h} px, 300 DPI)")

    # 3. Copy to brain artifact directory for direct viewing/embedding
    shutil.copy(svg_pub, os.path.join(BRAIN_DIR, f"{name}.svg"))
    shutil.copy(png_pub, os.path.join(BRAIN_DIR, f"{name}.png"))

print("All Brand Assets successfully updated (Abuja removed)!")
