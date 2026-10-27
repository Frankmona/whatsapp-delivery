import os
import subprocess

workspace_dir = "/Users/user/Desktop/Whatsapp delivery"
simple_html = f"{workspace_dir}/scratch/simple_hiring_flyer.html"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

png_out = f"{workspace_dir}/public/images/fmxpress_simple_hiring_flyer.png"
pdf_out = f"{workspace_dir}/public/downloads/fmxpress_simple_hiring_flyer.pdf"

artifact_dir = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"

print("1. Rendering simple flyer PNG (1080x1350)...")
png_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_simple_profile",
    "--window-size=1080,1350",
    "--hide-scrollbars",
    f"--screenshot={png_out}",
    f"file://{simple_html}"
]
subprocess.run(png_cmd, check=True)
print(f"Generated PNG: {png_out} ({os.path.getsize(png_out):,} bytes)")

print("2. Rendering simple flyer PDF...")
pdf_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_simple_profile",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out}",
    f"file://{simple_html}"
]
subprocess.run(pdf_cmd, check=True)
print(f"Generated PDF: {pdf_out} ({os.path.getsize(pdf_out):,} bytes)")

# Sync to artifacts
import shutil
shutil.copy(png_out, f"{artifact_dir}/fmxpress_simple_hiring_flyer.png")
shutil.copy(pdf_out, f"{artifact_dir}/fmxpress_simple_hiring_flyer.pdf")
print("Synced to artifacts!")
