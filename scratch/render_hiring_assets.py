import os
import subprocess
import zipfile
import shutil

workspace_dir = "/Users/user/Desktop/Whatsapp delivery"
social_html = f"{workspace_dir}/scratch/hiring_flyer_1080x1350.html"
canvas_html = f"{workspace_dir}/scratch/hiring_canvas.html"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(f"{workspace_dir}/public/downloads", exist_ok=True)
os.makedirs(f"{workspace_dir}/public/images", exist_ok=True)

pdf_out = f"{workspace_dir}/public/downloads/fmxpress_hiring_flyer_a5.pdf"
png_300dpi_out = f"{workspace_dir}/public/images/fmxpress_hiring_flyer_a5_300dpi.png"
png_social_out = f"{workspace_dir}/public/images/fmxpress_hiring_flyer_social.png"
zip_out = f"{workspace_dir}/public/downloads/FM_XPRESS_Dispatch_Rider_Hiring_Kit.zip"

artifact_dir = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"

print("1. Generating Social Media Flyer (1080x1350) via Headless Chrome...")
social_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_hiring_profile",
    "--window-size=1080,1350",
    "--hide-scrollbars",
    f"--screenshot={png_social_out}",
    f"file://{social_html}"
]
subprocess.run(social_cmd, check=True)
print(f"-> Generated Social Media PNG: {png_social_out} ({os.path.getsize(png_social_out):,} bytes)")

print("2. Generating Vector Print PDF (A5) via Headless Chrome...")
pdf_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_hiring_profile",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out}",
    f"file://{canvas_html}"
]
subprocess.run(pdf_cmd, check=True)
print(f"-> Generated PDF: {pdf_out} ({os.path.getsize(pdf_out):,} bytes)")

print("3. Generating High-Res Print PNG from Social Master...")
# Sizing social master to 300 DPI A5 scale
from PIL import Image
with Image.open(png_social_out) as img:
    # Scale to 1819 x 2274 and pad to 1819 x 2551 for full bleed A5
    scaled = img.resize((1819, int(1819 * 1350 / 1080)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (1819, 2551), (2, 6, 23, 255))
    offset_y = (2551 - scaled.height) // 2
    canvas.paste(scaled, (0, offset_y))
    canvas.save(png_300dpi_out, "PNG", dpi=(300, 300))
    print(f"-> Generated 300 DPI A5 PNG: {png_300dpi_out} ({os.path.getsize(png_300dpi_out):,} bytes)")

print("4. Packing Complete Hiring Kit ZIP...")
readme_path = f"{workspace_dir}/scratch/README_HIRING_SPECIFICATIONS.txt"
with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(pdf_out, "01_PRINT_READY_PDF/fmxpress_hiring_flyer_a5.pdf")
    z.write(png_300dpi_out, "02_HIGH_RES_300DPI_PNG/fmxpress_hiring_flyer_a5_300dpi.png")
    z.write(png_social_out, "03_SOCIAL_MEDIA_1080x1350/fmxpress_hiring_flyer_social.png")
    z.write(f"{workspace_dir}/public/images/fmxpress_simple_hiring_flyer.png", "03_SOCIAL_MEDIA_1080x1350/fmxpress_simple_hiring_flyer.png")
    z.write(f"{workspace_dir}/public/downloads/fmxpress_simple_hiring_flyer.pdf", "01_PRINT_READY_PDF/fmxpress_simple_hiring_flyer.pdf")
    z.write(f"{workspace_dir}/public/images/fmxpress_simple_hiring_banner.png", "05_LANDSCAPE_BANNER_1200x630/fmxpress_simple_hiring_banner.png")
    z.write(f"{workspace_dir}/public/downloads/fmxpress_simple_hiring_banner.pdf", "05_LANDSCAPE_BANNER_1200x630/fmxpress_simple_hiring_banner.pdf")
    z.write(f"{workspace_dir}/public/images/fmxpress_hiring_qr.png", "04_ASSETS/fmxpress_hiring_qr.png")
    z.write(f"{workspace_dir}/public/images/fmxpress_hiring_courier.jpg", "04_ASSETS/fmxpress_hiring_courier.jpg")
    z.write(readme_path, "README_HIRING_SPECIFICATIONS.txt")

print(f"-> Generated ZIP Kit: {zip_out} ({os.path.getsize(zip_out):,} bytes)")

print("5. Syncing to artifacts...")
shutil.copy(pdf_out, f"{artifact_dir}/fmxpress_hiring_flyer_a5.pdf")
shutil.copy(png_300dpi_out, f"{artifact_dir}/fmxpress_hiring_flyer_a5_300dpi.png")
shutil.copy(png_social_out, f"{artifact_dir}/fmxpress_hiring_flyer_social.png")
shutil.copy(f"{workspace_dir}/public/images/fmxpress_simple_hiring_flyer.png", f"{artifact_dir}/fmxpress_simple_hiring_flyer.png")
shutil.copy(f"{workspace_dir}/public/downloads/fmxpress_simple_hiring_flyer.pdf", f"{artifact_dir}/fmxpress_simple_hiring_flyer.pdf")
shutil.copy(f"{workspace_dir}/public/images/fmxpress_simple_hiring_banner.png", f"{artifact_dir}/fmxpress_simple_hiring_banner.png")
shutil.copy(f"{workspace_dir}/public/downloads/fmxpress_simple_hiring_banner.pdf", f"{artifact_dir}/fmxpress_simple_hiring_banner.pdf")
shutil.copy(zip_out, f"{artifact_dir}/FM_XPRESS_Dispatch_Rider_Hiring_Kit.zip")
print("ALL ASSETS SUCCESSFULLY GENERATED & SYNCED!")
