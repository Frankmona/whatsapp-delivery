import os
import subprocess
import shutil
import zipfile

PUBLIC_DIR = "public/images"
BRAIN_DIR = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"
PKG_DIR = "FM_XPRESS_Brand_Files"

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# =========================================================================
# 1. TEMPLATE GENERATOR FOR FULL 16:9 STUDIO T-SHIRT MOCKUP (FRONT & BACK)
# =========================================================================
def build_studio_mockup_svg(theme="black"):
    is_black = (theme == "black")
    bg_color = "#0B0F19" if is_black else "#F8FAFC"
    text_color = "#FFFFFF" if is_black else "#0F172A"
    sub_text = "#94A3B8" if is_black else "#64748B"
    badge_bg = "rgba(255,255,255,0.06)" if is_black else "rgba(15,23,42,0.06)"
    border_color = "rgba(255,255,255,0.12)" if is_black else "rgba(15,23,42,0.12)"

    # Shirt Gradients
    if is_black:
        body_fill = "url(#shirtBlackGrad)"
        body_stroke = "#334155"
        collar_fill = "#0F172A"
        collar_stroke = "#475569"
        front_fm = "#FFFFFF"
        back_fm = "#FFFFFF"
        back_phone = "#FFFFFF"
    else:
        body_fill = "url(#shirtWhiteGrad)"
        body_stroke = "#CBD5E1"
        collar_fill = "#F1F5F9"
        collar_stroke = "#94A3B8"
        front_fm = "#0F172A"
        back_fm = "#0F172A"
        back_phone = "#0F172A"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="3200" height="1800" viewBox="0 0 3200 1800">
  <defs>
    <!-- Background Gradients -->
    <radialGradient id="studioLighting" cx="50%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{ '#1E293B' if is_black else '#FFFFFF' }" />
      <stop offset="60%" stop-color="{ '#0F172A' if is_black else '#F1F5F9' }" />
      <stop offset="100%" stop-color="{ '#080C16' if is_black else '#E2E8F0' }" />
    </radialGradient>

    <!-- T-Shirt Body Gradients -->
    <linearGradient id="shirtBlackGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" />
      <stop offset="45%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#070A10" />
    </linearGradient>

    <linearGradient id="shirtWhiteGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="50%" stop-color="#F8FAFC" />
      <stop offset="100%" stop-color="#E2E8F0" />
    </linearGradient>

    <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>

    <!-- Soft Drop Shadows -->
    <filter id="shirtShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="25" stdDeviation="35" flood-color="#000000" flood-opacity="0.45" />
    </filter>
    <filter id="badgeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#000000" flood-opacity="0.35" />
    </filter>
  </defs>

  <!-- STUDIO BACKGROUND -->
  <rect width="3200" height="1800" fill="url(#studioLighting)"/>
  
  <!-- Subtle Studio Floor Grid / Platform Lines -->
  <line x1="200" y1="1620" x2="3000" y2="1620" stroke="{border_color}" stroke-width="2"/>

  <!-- ================= TOP HEADER BAR ================= -->
  <g transform="translate(1600, 95)" text-anchor="middle">
    <text font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="44" letter-spacing="4" fill="{text_color}">
      FM <tspan fill="#10B981">XPRESS</tspan> OFFICIAL DISPATCH UNIFORM
    </text>
    <text y="42" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="700" font-size="22" letter-spacing="8" fill="#10B981">
      { 'BLACK EDITION' if is_black else 'WHITE EDITION' } • 100% COMBED COTTON (200 GSM)
    </text>
  </g>

  <!-- VIEW LABELS -->
  <!-- Left: FRONT VIEW -->
  <g transform="translate(900, 195)" text-anchor="middle">
    <rect x="-180" y="-32" width="360" height="52" rx="26" fill="{badge_bg}" stroke="{border_color}" stroke-width="1.5"/>
    <text y="4" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="20" letter-spacing="4" fill="{text_color}">
      FRONT CHEST PRINT
    </text>
  </g>

  <!-- Right: BACK VIEW -->
  <g transform="translate(2300, 195)" text-anchor="middle">
    <rect x="-240" y="-32" width="480" height="52" rx="26" fill="{badge_bg}" stroke="{border_color}" stroke-width="1.5"/>
    <text y="4" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="20" letter-spacing="4" fill="{text_color}">
      BACK VIEW • <tspan fill="#10B981">WHATSAPP QR CODE</tspan>
    </text>
  </g>

  <!-- =================================================== -->
  <!-- LEFT: FRONT VIEW T-SHIRT (WITH BIKE SIGN LOGO)       -->
  <!-- =================================================== -->
  <g transform="translate(270, 240) scale(4.2)" filter="url(#shirtShadow)">
    <!-- T-Shirt Body Silhouette -->
    <path d="
      M 115 28
      C 125 54, 175 54, 185 28
      L 235 46
      L 282 104
      L 248 126
      L 225 100
      L 225 285
      L 75 285
      L 75 100
      L 52 126
      L 18 104
      L 65 46
      Z"
      fill="{body_fill}"
      stroke="{body_stroke}"
      stroke-width="1.5"
    />

    <!-- Crewneck Front Collar Rib -->
    <path d="
      M 115 28
      C 125 54, 175 54, 185 28
      C 178 36, 122 36, 115 28
      Z"
      fill="{collar_fill}"
      stroke="{collar_stroke}"
      stroke-width="1.5"
    />

    <!-- Sleeve & Hem Stitch Lines -->
    <path d="M 225 100 L 235 46" stroke="{collar_stroke}" stroke-width="0.75" stroke-dasharray="2,2" opacity="0.4"/>
    <path d="M 75 100 L 65 46" stroke="{collar_stroke}" stroke-width="0.75" stroke-dasharray="2,2" opacity="0.4"/>
    <line x1="77" y1="278" x2="223" y2="278" stroke="{collar_stroke}" stroke-width="0.75" stroke-dasharray="3,2" opacity="0.4"/>

    <!-- FRONT CHEST LOGO (Squircle Bike Sign + FM XPRESS) -->
    <g transform="translate(86, 102)">
      <!-- SQUIRCLE BIKE COURIER EMBLEM -->
      <g transform="scale(0.125)">
        <rect x="0" y="0" width="280" height="280" rx="70" fill="url(#emeraldGrad)" />
        <rect x="7" y="7" width="266" height="266" rx="63" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.4" />

        <!-- Speed Lines -->
        <path d="M 32 118 L 86 118" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.45" />
        <path d="M 20 150 L 78 150" stroke="#FFFFFF" stroke-width="8.5" stroke-linecap="round" opacity="0.8" />
        <path d="M 38 182 L 92 182" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.45" />

        <!-- Wheels -->
        <circle cx="98" cy="198" r="30" fill="#0B1329" stroke="#FFFFFF" stroke-width="7.5"/>
        <circle cx="98" cy="198" r="12" fill="#10B981"/>
        <circle cx="210" cy="198" r="30" fill="#0B1329" stroke="#FFFFFF" stroke-width="7.5"/>
        <circle cx="210" cy="198" r="12" fill="#10B981"/>

        <!-- Motorcycle Chassis & Fork -->
        <path d="M 98 198 L 136 170 L 172 170 L 210 198 L 188 158 L 145 158 Z" fill="#FFFFFF"/>
        <path d="M 210 198 L 180 130 L 164 133" stroke="#FFFFFF" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 180 130 L 196 112 L 182 110 Z" fill="#A7F3D0"/>

        <!-- Insulated Delivery Box -->
        <rect x="76" y="126" width="46" height="44" rx="9" fill="#FFFFFF" stroke="#0B1329" stroke-width="4.5"/>
        <path d="M 85 148 L 113 148" stroke="#10B981" stroke-width="5.5" stroke-linecap="round"/>

        <!-- Courier Rider -->
        <path d="M 112 150 C 120 128, 138 122, 162 134 L 176 148 L 162 164 L 138 159 Z" fill="#0B1329"/>
        <path d="M 144 137 L 170 144 L 176 135" stroke="#0B1329" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <circle cx="155" cy="109" r="21" fill="#0B1329" stroke="#FFFFFF" stroke-width="3"/>
        <path d="M 160 101 C 170 103, 172 113, 170 119 L 160 117 Z" fill="#34D399"/>
      </g>

      <!-- TYPOGRAPHY RIGHT OF EMBLEM -->
      <g transform="translate(44, 16)">
        <text x="0" y="0" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="16.5" fill="{front_fm}">FM</text>
        <text x="28" y="0" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="16.5" fill="#10B981">XPRESS</text>
        <text x="0" y="8.5" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="800" font-size="4.4" fill="{sub_text}" letter-spacing="1.4">DISPATCH &amp; LOGISTICS</text>
        <text x="0" y="15.5" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="700" font-size="3.8" fill="#10B981" letter-spacing="0.5">Your Package. Our Priority.</text>
      </g>
    </g>
  </g>

  <!-- =================================================== -->
  <!-- RIGHT: BACK VIEW T-SHIRT (WITH WHATSAPP QR CODE)    -->
  <!-- =================================================== -->
  <g transform="translate(1670, 240) scale(4.2)" filter="url(#shirtShadow)">
    <!-- T-Shirt Body Silhouette (Back) -->
    <path d="
      M 115 28
      C 130 36, 170 36, 185 28
      L 235 46
      L 282 104
      L 248 126
      L 225 100
      L 225 285
      L 75 285
      L 75 100
      L 52 126
      L 18 104
      L 65 46
      Z"
      fill="{body_fill}"
      stroke="{body_stroke}"
      stroke-width="1.5"
    />

    <!-- Crewneck Back Collar Band -->
    <path d="
      M 115 28
      C 130 36, 170 36, 185 28
      L 183 23
      C 170 31, 130 31, 117 23
      Z"
      fill="{collar_fill}"
      stroke="{collar_stroke}"
      stroke-width="1.5"
    />

    <!-- Hem Stitch Line -->
    <line x1="77" y1="278" x2="223" y2="278" stroke="{collar_stroke}" stroke-width="0.75" stroke-dasharray="3,2" opacity="0.4"/>

    <!-- BACK BRAND GRAPHIC, QR CODE, BRAND PROMISE & PHONE -->
    <g transform="translate(150, 48)">
      <!-- Upper Shoulder FM XPRESS -->
      <g transform="translate(0, 0)">
        <text x="-38" y="0" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="15" fill="{back_fm}">FM</text>
        <text x="-12" y="0" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="15" fill="#10B981">XPRESS</text>
      </g>
      <text x="0" y="8.5" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="800" font-size="4.6" fill="{back_fm}" letter-spacing="0.5" opacity="0.95">
        YOUR PACKAGE. OUR PRIORITY.
      </text>
      <text x="0" y="16.5" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="800" font-size="4.8" fill="#10B981" letter-spacing="1.2">
        CHAT &amp; BOOK ON WHATSAPP
      </text>

      <!-- Crisp White QR Code Badge -->
      <g transform="translate(-38, 20)" filter="url(#badgeShadow)">
        <rect width="76" height="80" rx="8" fill="#FFFFFF"/>
        
        <!-- Finder Patterns -->
        <rect x="8" y="7" width="16" height="16" fill="#0F172A" rx="2"/>
        <rect x="10.5" y="9.5" width="11" height="11" fill="#FFFFFF" rx="1"/>
        <rect x="12.5" y="11.5" width="7" height="7" fill="#0F172A" rx="0.5"/>

        <rect x="52" y="7" width="16" height="16" fill="#0F172A" rx="2"/>
        <rect x="54.5" y="9.5" width="11" height="11" fill="#FFFFFF" rx="1"/>
        <rect x="56.5" y="11.5" width="7" height="7" fill="#0F172A" rx="0.5"/>

        <rect x="8" y="47" width="16" height="16" fill="#0F172A" rx="2"/>
        <rect x="10.5" y="49.5" width="11" height="11" fill="#FFFFFF" rx="1"/>
        <rect x="12.5" y="51.5" width="7" height="7" fill="#0F172A" rx="0.5"/>

        <!-- QR Data Matrix Dots -->
        <rect x="27" y="7" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="35" y="7" width="5.5" height="4.5" fill="#0F172A"/>
        <rect x="44" y="7" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="27" y="15" width="5.5" height="4.5" fill="#0F172A"/>
        <rect x="36" y="15" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="44" y="15" width="5" height="4.5" fill="#0F172A"/>
        <rect x="8" y="27" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="16" y="27" width="4.5" height="4.5" fill="#0F172A"/>
        
        <!-- Center Emerald Brand Target inside QR -->
        <rect x="26" y="26" width="7" height="7" fill="#10B981" rx="1.5"/>
        <rect x="36" y="26" width="7" height="7" fill="#10B981" rx="1.5"/>
        <rect x="46" y="26" width="7" height="7" fill="#10B981" rx="1.5"/>
        
        <rect x="56" y="27" width="5.5" height="4.5" fill="#0F172A"/>
        <rect x="64" y="27" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="27" y="37" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="35" y="37" width="6.5" height="4.5" fill="#0F172A"/>
        <rect x="45" y="37" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="27" y="46" width="5.5" height="4.5" fill="#0F172A"/>
        <rect x="36" y="46" width="5.5" height="4.5" fill="#0F172A"/>
        <rect x="45" y="46" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="54" y="46" width="4.5" height="4.5" fill="#0F172A"/>
        <rect x="63" y="46" width="5" height="4.5" fill="#0F172A"/>
        <rect x="27" y="55" width="4.5" height="5.5" fill="#0F172A"/>
        <rect x="36" y="55" width="5.5" height="5.5" fill="#0F172A"/>
        <rect x="46" y="55" width="5.5" height="5.5" fill="#0F172A"/>
        <rect x="56" y="55" width="4.5" height="5.5" fill="#0F172A"/>

        <!-- Scan Label -->
        <text x="38" y="73" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="4.2" fill="#0F172A" text-anchor="middle" letter-spacing="0.2">
          SCAN TO BOOK ON WHATSAPP
        </text>
      </g>

      <!-- BRAND PROMISE -->
      <text x="0" y="113" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="800" font-size="5.2" fill="#10B981" letter-spacing="1.2">
        FAST • RELIABLE • CONVENIENT
      </text>

      <!-- Phone Number & Website -->
      <text x="0" y="124" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="10.5" fill="{back_phone}" letter-spacing="0.8">
        0903 686 9830
      </text>
      <text x="0" y="132" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="600" font-size="5.2" fill="{sub_text}" letter-spacing="0.5">
        fmxpress.tekvolutionhq.com
      </text>
    </g>
  </g>

  <!-- ================= BOTTOM SPECS BAR ================= -->
  <g transform="translate(1600, 1690)" text-anchor="middle">
    <text font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="800" font-size="19" letter-spacing="3" fill="{sub_text}">
      FRONT: 26CM BIKE SIGN PRINT • BACK: WHATSAPP QR MAGNET • DTF / SCREEN PRINT READY (300 DPI)
    </text>
  </g>
</svg>"""
    return svg

# =========================================================================
# 2. GENERATE AND CONVERT MOCKUPS TO HIGH-RES PNG & JPEG
# =========================================================================
mockups = [
    ("fmxpress_tshirt_black_mockup", build_studio_mockup_svg("black")),
    ("fmxpress_tshirt_white_mockup", build_studio_mockup_svg("white")),
]

for name, svg_content in mockups:
    svg_file = f"scratch/{name}.svg"
    png_file = f"{PUBLIC_DIR}/{name}.png"
    jpg_file = f"{PUBLIC_DIR}/{name}.jpg"

    with open(svg_file, "w") as f:
        f.write(svg_content)

    # Render 3,200 x 1,800 px at 300 DPI via sips
    subprocess.run([
        "sips", "-s", "format", "png",
        "-s", "dpiHeight", "300.0",
        "-s", "dpiWidth", "300.0",
        "-z", "1800", "3200",
        svg_file, "--out", png_file
    ], check=True)

    # Convert to JPEG for smaller file size & universal viewing
    subprocess.run([
        "sips", "-s", "format", "jpeg",
        "-s", "formatOptions", "92",
        png_file, "--out", jpg_file
    ], check=True)

    print(f"Generated: {jpg_file} and {png_file} (3200x1800 px, 300 DPI)")

    # Copy to brain artifact dir
    shutil.copy(jpg_file, os.path.join(BRAIN_DIR, f"{name}.jpg"))
    shutil.copy(png_file, os.path.join(BRAIN_DIR, f"{name}.png"))

# =========================================================================
# 3. UPDATE FM_XPRESS_Brand_Files FOLDER AND RE-ZIP
# =========================================================================
mockup_dir = f"{PKG_DIR}/03_Mockups_Visual_Previews"
os.makedirs(mockup_dir, exist_ok=True)

# Copy the CORRECT mockups into the package folder
shutil.copy(f"{PUBLIC_DIR}/fmxpress_tshirt_black_mockup.jpg", f"{mockup_dir}/fmxpress_tshirt_black_mockup.jpg")
shutil.copy(f"{PUBLIC_DIR}/fmxpress_tshirt_black_mockup.png", f"{mockup_dir}/fmxpress_tshirt_black_mockup.png")
shutil.copy(f"{PUBLIC_DIR}/fmxpress_tshirt_white_mockup.jpg", f"{mockup_dir}/fmxpress_tshirt_white_mockup.jpg")
shutil.copy(f"{PUBLIC_DIR}/fmxpress_tshirt_white_mockup.png", f"{mockup_dir}/fmxpress_tshirt_white_mockup.png")
if os.path.exists(f"{PUBLIC_DIR}/fmxpress_cap_mockup.jpg"):
    shutil.copy(f"{PUBLIC_DIR}/fmxpress_cap_mockup.jpg", f"{mockup_dir}/fmxpress_cap_mockup.jpg")

# Re-create the ZIP file with the correct mockups!
zip_dest = "public/FM_XPRESS_Brand_Files.zip"
with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(PKG_DIR):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, ".")
            zipf.write(full_p, rel_p)

print("ZIP updated with the correct mockups!")
