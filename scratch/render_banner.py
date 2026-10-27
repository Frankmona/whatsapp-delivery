import os
import subprocess
import shutil

workspace_dir = "/Users/user/Desktop/Whatsapp delivery"
banner_html = f"{workspace_dir}/scratch/simple_banner.html"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

png_out = f"{workspace_dir}/public/images/fmxpress_simple_hiring_banner.png"
pdf_out = f"{workspace_dir}/public/downloads/fmxpress_simple_hiring_banner.pdf"

artifact_dir = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"

print("1. Rendering simple banner PNG (1200x630)...")
png_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_banner_profile",
    "--window-size=1200,630",
    "--hide-scrollbars",
    f"--screenshot={png_out}",
    f"file://{banner_html}"
]
subprocess.run(png_cmd, check=True)
print(f"Generated PNG: {png_out} ({os.path.getsize(png_out):,} bytes)")

print("2. Rendering simple banner PDF...")
pdf_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_banner_profile",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out}",
    f"file://{banner_html}"
]
subprocess.run(pdf_cmd, check=True)
print(f"Generated PDF: {pdf_out} ({os.path.getsize(pdf_out):,} bytes)")

# Sync to artifacts
shutil.copy(png_out, f"{artifact_dir}/fmxpress_simple_hiring_banner.png")
shutil.copy(pdf_out, f"{artifact_dir}/fmxpress_simple_hiring_banner.pdf")
print("Synced to artifacts!")
