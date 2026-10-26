import os
import subprocess
import shutil
import zipfile

PUBLIC_DIR = "public/images"
BRAIN_DIR = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"
PKG_DIR = "FM_XPRESS_Brand_Files"

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)
os.makedirs(f"{PKG_DIR}/01_Logos_Official_300DPI", exist_ok=True)
os.makedirs(f"{PKG_DIR}/02_Apparel_Print_Files_300DPI", exist_ok=True)
os.makedirs(f"{PKG_DIR}/03_Mockups_Visual_Previews", exist_ok=True)

# 1. CAP EMBROIDERY PATCH SVG (2400 x 2400 transparent canvas)
cap_patch_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="2400" viewBox="0 0 2400 2400">
  <defs>
    <linearGradient id="capGrad2400" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>
  </defs>

  <!-- CAP EMBROIDERY PATCH -->
  <g transform="translate(300, 300)">
    <!-- Base Squircle with Merrowed Border -->
    <rect x="0" y="0" width="1800" height="1800" rx="450" fill="url(#capGrad2400)" />
    <!-- Outer Raised Edge -->
    <rect x="24" y="24" width="1752" height="1752" rx="426" fill="none" stroke="#A7F3D0" stroke-width="16" opacity="0.6"/>
    <!-- Inner Stitch Line -->
    <rect x="56" y="56" width="1688" height="1688" rx="394" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-dasharray="20,16" opacity="0.5"/>

    <!-- TOP TYPOGRAPHY: FM XPRESS EST. 2023 -->
    <text x="900" y="420" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="164" letter-spacing="6" fill="#FFFFFF">FM XPRESS</text>
    <text x="900" y="516" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="700" font-size="52" letter-spacing="16" fill="#D1FAE5" opacity="0.9">EST. 2023</text>

    <!-- MOTORCYCLE COURIER EMBLEM -->
    <g transform="translate(900, 1120)">
      <!-- Speed Lines -->
      <path d="M -580 -160 L -340 -160" stroke="#FFFFFF" stroke-width="36" stroke-linecap="round" opacity="0.45" />
      <path d="M -640 0 L -360 0" stroke="#FFFFFF" stroke-width="44" stroke-linecap="round" opacity="0.85" />
      <path d="M -540 160 L -300 160" stroke="#FFFFFF" stroke-width="36" stroke-linecap="round" opacity="0.45" />

      <!-- Rear Wheel -->
      <circle cx="-270" cy="240" r="152" fill="#0B1329" stroke="#FFFFFF" stroke-width="36"/>
      <circle cx="-270" cy="240" r="60" fill="#10B981"/>

      <!-- Front Wheel -->
      <circle cx="300" cy="240" r="152" fill="#0B1329" stroke="#FFFFFF" stroke-width="36"/>
      <circle cx="300" cy="240" r="60" fill="#10B981"/>

      <!-- Motorcycle Chassis -->
      <path d="M -270 240 L -80 100 L 110 100 L 300 240 L 180 40 L -40 40 Z" fill="#FFFFFF"/>

      <!-- Fork & Handlebars -->
      <path d="M 300 240 L 150 -100 L 70 -84" stroke="#FFFFFF" stroke-width="36" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <path d="M 150 -100 L 230 -190 L 160 -200 Z" fill="#A7F3D0"/>

      <!-- Delivery Box -->
      <rect x="-380 -120" width="240" height="224" rx="48" fill="#FFFFFF" stroke="#0B1329" stroke-width="24"/>
      <path d="M -336 -8 L -184 -8" stroke="#10B981" stroke-width="28" stroke-linecap="round"/>

      <!-- Courier Rider -->
      <path d="M -200 4 C -160 -104, -60 -140, 60 -80 L 132 -8 L 60 76 L -60 52 Z" fill="#0B1329"/>
      <path d="M -30 -60 L 100 -24 L 132 -70" stroke="#0B1329" stroke-width="44" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <circle cx="24" cy="-210" r="104" fill="#0B1329" stroke="#FFFFFF" stroke-width="16"/>
      <path d="M 48 -250 C 100 -240, 112 -190, 100 -160 L 48 -170 Z" fill="#34D399"/>
    </g>
  </g>
</svg>"""

# 2. CAP BIKE CREST SVG (2400 x 2400 transparent canvas)
cap_bike_crest_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="2400" viewBox="0 0 2400 2400">
  <defs>
    <linearGradient id="capCrestGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>
  </defs>

  <g transform="translate(300, 300)">
    <rect x="0" y="0" width="1800" height="1800" rx="450" fill="url(#capCrestGrad)" />
    <rect x="45" y="45" width="1710" height="1710" rx="405" fill="none" stroke="#FFFFFF" stroke-width="21" opacity="0.4" />

    <!-- Speed Lines -->
    <path d="M 210 750 L 540 750" stroke="#FFFFFF" stroke-width="45" stroke-linecap="round" opacity="0.45" />
    <path d="M 135 960 L 495 960" stroke="#FFFFFF" stroke-width="54" stroke-linecap="round" opacity="0.8" />
    <path d="M 255 1170 L 585 1170" stroke="#FFFFFF" stroke-width="45" stroke-linecap="round" opacity="0.45" />

    <!-- Wheels -->
    <circle cx="630" cy="1260" r="192" fill="#0B1329" stroke="#FFFFFF" stroke-width="48"/>
    <circle cx="630" cy="1260" r="78" fill="#10B981"/>
    
    <circle cx="1350" cy="1260" r="192" fill="#0B1329" stroke="#FFFFFF" stroke-width="48"/>
    <circle cx="1350" cy="1260" r="78" fill="#10B981"/>

    <!-- Chassis & Fork -->
    <path d="M 630 1260 L 870 1080 L 1110 1080 L 1350 1260 L 1200 1005 L 930 1005 Z" fill="#FFFFFF"/>
    <path d="M 1350 1260 L 1155 825 L 1050 846" stroke="#FFFFFF" stroke-width="48" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <path d="M 1155 825 L 1260 708 L 1170 696 Z" fill="#A7F3D0"/>

    <!-- Delivery Box -->
    <rect x="480" y="804" width="300" height="282" rx="60" fill="#FFFFFF" stroke="#0B1329" stroke-width="30"/>
    <path d="M 540 945 L 720 945" stroke="#10B981" stroke-width="36" stroke-linecap="round"/>

    <!-- Courier Rider -->
    <path d="M 720 960 C 768 822, 888 780, 1038 858 L 1128 948 L 1038 1050 L 888 1020 Z" fill="#0B1329"/>
    <path d="M 930 876 L 1092 924 L 1134 864" stroke="#0B1329" stroke-width="54" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <circle cx="996" cy="696" r="132" fill="#0B1329" stroke="#FFFFFF" stroke-width="19.5"/>
    <path d="M 1026 648 C 1092 660, 1104 726, 1092 762 L 1026 750 Z" fill="#34D399"/>
  </g>
</svg>"""

# Save SVGs
files_to_render = [
    # 02 Apparel Print Files
    (f"{PKG_DIR}/02_Apparel_Print_Files_300DPI/fmxpress_cap_embroidery_patch.svg",
     f"{PKG_DIR}/02_Apparel_Print_Files_300DPI/fmxpress_cap_embroidery_patch.png",
     cap_patch_svg),
    (f"{PKG_DIR}/02_Apparel_Print_Files_300DPI/fmxpress_cap_bike_crest.svg",
     f"{PKG_DIR}/02_Apparel_Print_Files_300DPI/fmxpress_cap_bike_crest.png",
     cap_bike_crest_svg),

    # 01 Logos Official
    (f"{PKG_DIR}/01_Logos_Official_300DPI/fmxpress_cap_patch_logo.svg",
     f"{PKG_DIR}/01_Logos_Official_300DPI/fmxpress_cap_patch_logo.png",
     cap_patch_svg),
]

for svg_path, png_path, content in files_to_render:
    with open(svg_path, "w") as f:
        f.write(content)
    subprocess.run([
        "sips", "-s", "format", "png",
        "-s", "dpiHeight", "300.0",
        "-s", "dpiWidth", "300.0",
        "-z", "2400", "2400",
        svg_path, "--out", png_path
    ], check=True)
    
    # Mirror to public and brain
    basename = os.path.basename(png_path)
    shutil.copy(png_path, os.path.join(PUBLIC_DIR, basename))
    shutil.copy(svg_path, os.path.join(PUBLIC_DIR, os.path.basename(svg_path)))
    shutil.copy(png_path, os.path.join(BRAIN_DIR, basename))
    shutil.copy(svg_path, os.path.join(BRAIN_DIR, os.path.basename(svg_path)))
    print(f"Generated cap logo: {png_path}")

# 3. WRITE A PRODUCTION README FOR VENDORS & USERS
readme_text = """========================================================================
FM XPRESS — OFFICIAL BRAND & MERCHANDISE PRODUCTION ASSETS (300 DPI)
========================================================================
Brand Tagline:  Your Package. Our Priority.
Brand Promise:  Fast. Reliable. Convenient.
Contact/Book:   0903 686 9830 | fmxpress.tekvolutionhq.com
========================================================================

All files in this package are high-resolution 300 DPI print-ready vectors
(SVG) and transparent PNGs. Every asset is free of regional restrictions
for universal national dispatch operations.

------------------------------------------------------------------------
FOLDER 01: LOGOS (OFFICIAL 300 DPI)
------------------------------------------------------------------------
- fmxpress_logo_dark.png / .svg
  Horizontal primary logo with dark slate "FM" & emerald "XPRESS".
  Best for: White/light shirts, letterheads, websites, stationery.

- fmxpress_logo_light.png / .svg
  Horizontal primary logo with crisp white "FM" & emerald "XPRESS".
  Best for: Black/dark apparel, dark vehicle decals, signage.

- fmxpress_logo_all_white.png / .svg
  Monochromatic white version for single-color heat vinyl or stamps.

- fmxpress_badge_crest.png / .svg
  Standalone Squircle Speed Bike Courier Emblem without text.

- fmxpress_badge_stacked.png / .svg
  Stacked emblem + "FM XPRESS" + "DISPATCH & LOGISTICS" (for light backgrounds).

- fmxpress_badge_stacked_dark.png / .svg
  Stacked emblem + "FM XPRESS" + "DISPATCH & LOGISTICS" (for dark backgrounds).

- fmxpress_cap_patch_logo.png / .svg
  *** CAP LOGO *** (Squircle Patch with "FM XPRESS EST. 2023" + Bike Emblem).

------------------------------------------------------------------------
FOLDER 02: APPAREL PRINT FILES (DIRECT-TO-GARMENT / SCREEN / EMBROIDERY)
------------------------------------------------------------------------
- fmxpress_cap_embroidery_patch.png / .svg
  *** PRIMARY CAP PRODUCTION FILE ***
  High-res (2,400 x 2,400 px, 300 DPI) embroidery patch graphic as shown
  on the official FM Xpress cap mockup. Includes merrowed stitch border,
  "FM XPRESS EST. 2023", and speed bike courier.
  Production Technique: 3D Puff Embroidery or Woven Merrowed Patch (6cm x 6cm).

- fmxpress_cap_bike_crest.png / .svg
  *** MINIMAL CAP / HELMET EMBLEM ***
  Pure squircle speed courier emblem without typography.
  Production Technique: Flat embroidery, side crown embroidery, helmet decals.

- fmxpress_tshirt_front_print_dark.png / .svg
  T-SHIRT FRONT CHEST (FOR BLACK SHIRTS): Centered stacked squircle bike
  emblem + bold "FM XPRESS" + "DISPATCH & LOGISTICS" + "Your Package. Our Priority."

- fmxpress_tshirt_front_print_light.png / .svg
  T-SHIRT FRONT CHEST (FOR WHITE SHIRTS): Centered stacked squircle bike
  emblem + bold "FM XPRESS" + "DISPATCH & LOGISTICS" + "Your Package. Our Priority."

- fmxpress_tshirt_back_qr_dark.png / .svg
  T-SHIRT BACK (FOR BLACK SHIRTS): High-contrast white scannable WhatsApp
  booking QR code badge, "CHAT & BOOK ON WHATSAPP", "FAST • RELIABLE • CONVENIENT",
  and phone "0903 686 9830".

- fmxpress_tshirt_back_qr_light.png / .svg
  T-SHIRT BACK (FOR WHITE SHIRTS): Scannable WhatsApp booking QR code badge,
  brand promise, and direct contact details.

------------------------------------------------------------------------
FOLDER 03: MOCKUPS (VISUAL PREVIEWS)
------------------------------------------------------------------------
- fmxpress_cap_mockup.jpg
  High-resolution 3D studio mockup of the official black courier cap.

- fmxpress_tshirt_black_mockup.jpg / .png
  16:9 studio presentation (3,200 x 1,800 px, 300 DPI) of the black t-shirt
  showing front stacked chest print and back WhatsApp QR code.

- fmxpress_tshirt_white_mockup.jpg / .png
  16:9 studio presentation (3,200 x 1,800 px, 300 DPI) of the white t-shirt
  showing front stacked chest print and back WhatsApp QR code.

========================================================================
"""

with open(f"{PKG_DIR}/README_PRINT_GUIDE.txt", "w") as f:
    f.write(readme_text)

# 4. RE-BUILD ZIP FILE
zip_dest = "public/FM_XPRESS_Brand_Files.zip"
with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(PKG_DIR):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, ".")
            zipf.write(full_p, rel_p)

print("Package ZIP successfully rebuilt with explicitly labeled CAP logos and production guide!")
