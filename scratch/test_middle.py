import subprocess

svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 300 200">
  <rect width="300" height="200" fill="#0B0F19"/>
  <circle cx="150" cy="50" r="2" fill="red"/>
  <text x="150" y="50" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="800" font-size="10" fill="#94A3B8" letter-spacing="3">DISPATCH &amp; LOGISTICS</text>
  <circle cx="150" cy="90" r="2" fill="red"/>
  <text x="150" y="90" text-anchor="middle" font-family="-apple-system, 'SF Pro Display', Arial, sans-serif" font-weight="700" font-size="8" fill="#10B981" letter-spacing="1">Your Package. Our Priority.</text>
</svg>"""

with open("scratch/test_middle.svg", "w") as f:
    f.write(svg)

subprocess.run(["sips", "-s", "format", "png", "scratch/test_middle.svg", "--out", "scratch/test_middle.png"], check=True)
