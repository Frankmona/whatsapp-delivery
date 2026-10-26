import subprocess

svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1600" viewBox="0 0 300 300">
  <defs>
    <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>
    <linearGradient id="shirtBlackGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" />
      <stop offset="45%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#070A10" />
    </linearGradient>
  </defs>

  <rect width="300" height="300" fill="#0B0F19"/>

  <!-- T-SHIRT BODY -->
  <g transform="translate(0, 0)">
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
      fill="url(#shirtBlackGrad)"
      stroke="#334155"
      stroke-width="1.5"
    />
    <path d="
      M 115 28
      C 125 54, 175 54, 185 28
      C 178 36, 122 36, 115 28
      Z"
      fill="#0F172A"
      stroke="#475569"
      stroke-width="1.5"
    />

    <!-- FRONT CHEST STACKED LOGO -->
    <!-- Squircle Bike Courier Emblem (Centered at X=150) -->
    <!-- Emblem width: 280 * 0.16 = 44.8. Centered at 150: x = 150 - 22.4 = 127.6 -->
    <g transform="translate(127.6, 76) scale(0.16)">
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

    <!-- Typography directly below emblem -->
    <g transform="translate(150, 135)">
      <text x="-35" y="0" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="12" fill="#FFFFFF">FM</text>
      <text x="-15" y="0" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="900" font-size="12" fill="#10B981">XPRESS</text>
    </g>

    <text x="150" y="143" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="800" font-size="3.6" fill="#94A3B8" letter-spacing="1.4">DISPATCH &amp; LOGISTICS</text>
    <text x="150" y="149" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="700" font-size="3.2" fill="#10B981" letter-spacing="0.5">Your Package. Our Priority.</text>
  </g>
</svg>"""

with open("scratch/test_front_chest.svg", "w") as f:
    f.write(svg)

subprocess.run(["sips", "-s", "format", "png", "scratch/test_front_chest.svg", "--out", "scratch/test_front_chest.png"], check=True)
print("Rendered scratch/test_front_chest.png")
