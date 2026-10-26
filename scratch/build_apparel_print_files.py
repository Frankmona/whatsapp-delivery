import os
import subprocess
import shutil

PUBLIC_DIR = "public/images"
BRAIN_DIR = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# 1. FRONT CHEST PRINT WITH BIKE SIGN (For Black Shirts)
svg_front_dark = """<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="960" viewBox="0 0 2400 960">
  <defs>
    <linearGradient id="emeraldGradFront" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>
  </defs>

  <g transform="translate(180, 200)">
    <!-- SQUIRCLE BIKE COURIER EMBLEM -->
    <g transform="scale(1.95)">
      <rect x="0" y="0" width="280" height="280" rx="70" fill="url(#emeraldGradFront)" />
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

      <!-- Chassis & Fork -->
      <path d="M 98 198 L 136 170 L 172 170 L 210 198 L 188 158 L 145 158 Z" fill="#FFFFFF"/>
      <path d="M 210 198 L 180 130 L 164 133" stroke="#FFFFFF" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <path d="M 180 130 L 196 112 L 182 110 Z" fill="#A7F3D0"/>

      <!-- Delivery Box -->
      <rect x="76" y="126" width="46" height="44" rx="9" fill="#FFFFFF" stroke="#0B1329" stroke-width="4.5"/>
      <path d="M 85 148 L 113 148" stroke="#10B981" stroke-width="5.5" stroke-linecap="round"/>

      <!-- Rider -->
      <path d="M 112 150 C 120 128, 138 122, 162 134 L 176 148 L 162 164 L 138 159 Z" fill="#0B1329"/>
      <path d="M 144 137 L 170 144 L 176 135" stroke="#0B1329" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <circle cx="155" cy="109" r="21" fill="#0B1329" stroke="#FFFFFF" stroke-width="3"/>
      <path d="M 160 101 C 170 103, 172 113, 170 119 L 160 117 Z" fill="#34D399"/>
    </g>

    <!-- TYPOGRAPHY RIGHT OF EMBLEM -->
    <g transform="translate(640, 230)">
      <text y="0" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="220" letter-spacing="-5">
        <tspan fill="#FFFFFF">FM</tspan>
        <tspan fill="#10B981"> XPRESS</tspan>
      </text>
      <text y="110" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="800" font-size="58" fill="#94A3B8" letter-spacing="18">
        DISPATCH &amp; LOGISTICS
      </text>
      <path d="M 5 150 L 680 150" stroke="#10B981" stroke-width="10" stroke-linecap="round" />
      <text y="240" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="700" font-size="52" fill="#10B981" letter-spacing="6">
        Your Package. Our Priority.
      </text>
    </g>
  </g>
</svg>"""

# 1b. FRONT CHEST PRINT WITH BIKE SIGN (For White Shirts)
svg_front_light = svg_front_dark.replace('<tspan fill="#FFFFFF">FM</tspan>', '<tspan fill="#0F172A">FM</tspan>').replace('fill="#94A3B8"', 'fill="#475569"')

# 2. BACK VIEW PRINT WITH PURE QR CODE (For Black Shirts)
svg_back_black = """<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="3200" viewBox="0 0 2400 3200">
  <g transform="translate(1200, 320)" text-anchor="middle">
    <!-- Top FM XPRESS Brand -->
    <text y="0" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="200" letter-spacing="-4">
      <tspan fill="#FFFFFF">FM</tspan>
      <tspan fill="#10B981"> XPRESS</tspan>
    </text>
    <text y="95" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="800" font-size="52" fill="#FFFFFF" letter-spacing="8">
      YOUR PACKAGE. OUR PRIORITY.
    </text>
    <text y="180" font-family="-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif" font-weight="800" font-size="56" fill="#10B981" letter-spacing="12">
      CHAT &amp; BOOK ON WHATSAPP
    </text>

    <!-- White Card Container for PURE QR Code -->
    <g transform="translate(-600, 240)">
      <rect width="1200" height="1300" rx="100" fill="#FFFFFF"/>
      
      <!-- PURE HIGH RESOLUTION QR CODE -->
      <!-- Top Left Finder -->
      <rect x="120" y="100" width="240" height="240" fill="#0F172A" rx="30"/>
      <rect x="160" y="140" width="160" height="160" fill="#FFFFFF" rx="18"/>
      <rect x="195" y="175" width="90" height="90" fill="#0F172A" rx="12"/>

      <!-- Top Right Finder -->
      <rect x="840" y="100" width="240" height="240" fill="#0F172A" rx="30"/>
      <rect x="880" y="140" width="160" height="160" fill="#FFFFFF" rx="18"/>
      <rect x="915" y="175" width="90" height="90" fill="#0F172A" rx="12"/>

      <!-- Bottom Left Finder -->
      <rect x="120" y="760" width="240" height="240" fill="#0F172A" rx="30"/>
      <rect x="160" y="800" width="160" height="160" fill="#FFFFFF" rx="18"/>
      <rect x="195" y="835" width="90" height="90" fill="#0F172A" rx="12"/>

      <!-- QR Pattern Elements -->
      <rect x="420" y="100" width="70" height="70" fill="#0F172A"/>
      <rect x="540" y="100" width="80" height="70" fill="#0F172A"/>
      <rect x="670" y="100" width="70" height="70" fill="#0F172A"/>
      <rect x="420" y="210" width="80" height="70" fill="#0F172A"/>
      <rect x="550" y="210" width="70" height="70" fill="#0F172A"/>
      <rect x="710" y="210" width="80" height="70" fill="#0F172A"/>
      
      <!-- Central Emerald Brand Target inside QR -->
      <rect x="400" y="380" width="110" height="110" fill="#10B981" rx="20"/>
      <rect x="545" y="380" width="110" height="110" fill="#10B981" rx="20"/>
      <rect x="690" y="380" width="110" height="110" fill="#10B981" rx="20"/>

      <rect x="420" y="550" width="70" height="70" fill="#0F172A"/>
      <rect x="540" y="550" width="90" height="70" fill="#0F172A"/>
      <rect x="700" y="550" width="70" height="70" fill="#0F172A"/>
      <rect x="420" y="670" width="80" height="70" fill="#0F172A"/>
      <rect x="550" y="670" width="80" height="70" fill="#0F172A"/>
      <rect x="680" y="670" width="70" height="70" fill="#0F172A"/>
      <rect x="800" y="670" width="70" height="70" fill="#0F172A"/>
      
      <rect x="420" y="790" width="70" height="80" fill="#0F172A"/>
      <rect x="540" y="790" width="80" height="80" fill="#0F172A"/>
      <rect x="690" y="790" width="80" height="80" fill="#0F172A"/>
      <rect x="830" y="790" width="70" height="80" fill="#0F172A"/>
      <rect x="940" y="790" width="80" height="80" fill="#0F172A"/>
      <rect x="420" y="910" width="80" height="80" fill="#0F172A"/>
      <rect x="560" y="910" width="70" height="80" fill="#0F172A"/>
      <rect x="700" y="910" width="80" height="80" fill="#0F172A"/>
      <rect x="840" y="910" width="70" height="80" fill="#0F172A"/>

      <!-- Scan Call-to-Action -->
      <text x="600" y="1170" font-family="-apple-system, 'SF Pro Display', sans-serif" font-weight="900" font-size="70" fill="#0F172A" text-anchor="middle" letter-spacing="5">
        SCAN TO BOOK ON WHATSAPP
      </text>
    </g>

    <!-- Brand Promise -->
    <text y="1740" font-family="-apple-system, 'SF Pro Display', sans-serif" font-weight="900" font-size="64" fill="#10B981" letter-spacing="14">
      FAST • RELIABLE • CONVENIENT
    </text>

    <!-- Phone Number & Website -->
    <text y="1880" font-family="-apple-system, 'SF Pro Display', sans-serif" font-weight="900" font-size="145" fill="#FFFFFF" letter-spacing="8">
      0903 686 9830
    </text>
    <text y="1990" font-family="-apple-system, 'SF Pro Display', sans-serif" font-weight="700" font-size="70" fill="#64748B" letter-spacing="6">
      fmxpress.tekvolutionhq.com
    </text>
  </g>
</svg>"""

# 3. BACK VIEW PRINT WITH PURE QR CODE (For White Shirts - Dark typography)
svg_back_white = svg_back_black.replace(
    '<tspan fill="#FFFFFF">FM</tspan>', '<tspan fill="#0F172A">FM</tspan>'
).replace(
    'fill="#FFFFFF" letter-spacing="8">\n      YOUR PACKAGE. OUR PRIORITY.', 'fill="#0F172A" letter-spacing="8">\n      YOUR PACKAGE. OUR PRIORITY.'
).replace(
    'fill="#FFFFFF" letter-spacing="8">\n      0903 686 9830', 'fill="#0F172A" letter-spacing="8">\n      0903 686 9830'
)

manifest = [
    ("fmxpress_tshirt_front_print", svg_front_dark, 960, 2400),
    ("fmxpress_tshirt_front_print_dark", svg_front_dark, 960, 2400),
    ("fmxpress_tshirt_front_print_light", svg_front_light, 960, 2400),
    ("fmxpress_tshirt_back_qr_dark", svg_back_black, 3200, 2400),
    ("fmxpress_tshirt_back_qr_light", svg_back_white, 3200, 2400),
    # Also overwrite barcode filenames for backward compatibility with existing links
    ("fmxpress_tshirt_back_barcode_dark", svg_back_black, 3200, 2400),
    ("fmxpress_tshirt_back_barcode_light", svg_back_white, 3200, 2400),
]

for name, svg_content, h, w in manifest:
    svg_pub = os.path.join(PUBLIC_DIR, f"{name}.svg")
    with open(svg_pub, "w") as f:
        f.write(svg_content)
    
    png_pub = os.path.join(PUBLIC_DIR, f"{name}.png")
    subprocess.run([
        "sips", "-s", "format", "png",
        "-s", "dpiHeight", "300.0",
        "-s", "dpiWidth", "300.0",
        "-z", str(h), str(w),
        svg_pub, "--out", png_pub
    ], check=True)
    print(f"Generated 300 DPI: {png_pub}")

    shutil.copy(svg_pub, os.path.join(BRAIN_DIR, f"{name}.svg"))
    shutil.copy(png_pub, os.path.join(BRAIN_DIR, f"{name}.png"))

print("Apparel print files ready!")
