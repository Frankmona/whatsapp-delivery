import os
import subprocess
import zipfile
import shutil
from PIL import Image

workspace_dir = "/Users/user/Desktop/Whatsapp delivery"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(f"{workspace_dir}/public/downloads", exist_ok=True)
os.makedirs(f"{workspace_dir}/public/images", exist_ok=True)

rear_html = f"{workspace_dir}/scratch/box_rear_flyer_40x40.html"
side_html = f"{workspace_dir}/scratch/box_side_flyer_45x35.html"

rear_png = f"{workspace_dir}/public/images/fmxpress_box_rear_flyer_40x40.png"
rear_pdf = f"{workspace_dir}/public/downloads/fmxpress_box_rear_flyer_40x40.pdf"
rear_300dpi = f"{workspace_dir}/public/images/fmxpress_box_rear_300dpi.png"

side_png = f"{workspace_dir}/public/images/fmxpress_box_side_flyer_45x35.png"
side_pdf = f"{workspace_dir}/public/downloads/fmxpress_box_side_flyer_45x35.pdf"
side_300dpi = f"{workspace_dir}/public/images/fmxpress_box_side_300dpi.png"

zip_out = f"{workspace_dir}/public/downloads/FM_XPRESS_Dispatch_Box_Print_Kit.zip"
artifact_dir = "/Users/user/.gemini/antigravity/brain/82608a63-c28a-4f82-b547-85b2cfb6c711"

print("1. Rendering Rear Box Flyer (1600x1600) via Headless Chrome...")
subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_box_profile",
    "--window-size=1600,1600",
    "--hide-scrollbars",
    f"--screenshot={rear_png}",
    f"file://{rear_html}"
], check=True)
print(f"-> Saved Rear Box PNG: {rear_png} ({os.path.getsize(rear_png):,} bytes)")

print("2. Generating Vector Print PDF for Rear Box (400mm x 400mm)...")
subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_box_profile",
    "--no-pdf-header-footer",
    f"--print-to-pdf={rear_pdf}",
    f"file://{rear_html}"
], check=True)
print(f"-> Saved Rear Box PDF: {rear_pdf} ({os.path.getsize(rear_pdf):,} bytes)")

print("3. Rendering Side Box Flyer (1800x1400) via Headless Chrome...")
subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_box_profile",
    "--window-size=1800,1400",
    "--hide-scrollbars",
    f"--screenshot={side_png}",
    f"file://{side_html}"
], check=True)
print(f"-> Saved Side Box PNG: {side_png} ({os.path.getsize(side_png):,} bytes)")

print("4. Generating Vector Print PDF for Side Box (450mm x 350mm)...")
subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--user-data-dir=/tmp/chrome_box_profile",
    "--no-pdf-header-footer",
    f"--print-to-pdf={side_pdf}",
    f"file://{side_html}"
], check=True)
print(f"-> Saved Side Box PDF: {side_pdf} ({os.path.getsize(side_pdf):,} bytes)")

print("5. Generating 300 DPI Press-Ready Vinyl Masters via PIL...")
# Rear Box: 40cm x 40cm @ 300 DPI = 4724 x 4724 px
with Image.open(rear_png) as img:
    res = img.resize((4724, 4724), Image.Resampling.LANCZOS)
    res.save(rear_300dpi, "PNG", dpi=(300, 300))
    print(f"-> Saved Rear 300 DPI Master: {rear_300dpi} ({os.path.getsize(rear_300dpi):,} bytes)")

# Side Box: 45cm x 35cm @ 300 DPI = 5315 x 4134 px
with Image.open(side_png) as img:
    res = img.resize((5315, 4134), Image.Resampling.LANCZOS)
    res.save(side_300dpi, "PNG", dpi=(300, 300))
    print(f"-> Saved Side 300 DPI Master: {side_300dpi} ({os.path.getsize(side_300dpi):,} bytes)")

# 6. Create Vendor Specification Sheet
spec_path = f"{workspace_dir}/scratch/README_BOX_PRINT_SPECIFICATIONS.txt"
spec_content = """=============================================================================
FM XPRESS — DISPATCH CARGO DELIVERY BOX BRANDING & PRINT SPECIFICATIONS
=============================================================================

1. OVERVIEW & PURPOSE
-----------------------------------------------------------------------------
These assets are custom designed for standard motorcycle delivery cargo boxes
(70L - 90L fiberglass / molded ABS delivery boxes).
When riders are navigating Abuja and Kubwa roads, this design turns the delivery
box into a high-visibility mobile billboard with a prominent scannable QR code
and giant WhatsApp booking number.

2. ASSET INVENTORY & DIMENSIONS
-----------------------------------------------------------------------------
A. REAR BOX PANEL (Facing traffic & pedestrians behind motorcycle):
   - Standard Size: 40 cm x 40 cm (16 in x 16 in)
   - Vector PDF: fmxpress_box_rear_flyer_40x40.pdf (Infinitely Scalable)
   - High-Res Raster: fmxpress_box_rear_300dpi.png (4,724 x 4,724 px, 300 DPI)
   - Standard Web/Digital: fmxpress_box_rear_flyer_40x40.png (1,600 x 1,600 px)

B. SIDE BOX PANELS (Left and Right sides of cargo box):
   - Standard Size: 45 cm x 35 cm (18 in x 14 in)
   - Vector PDF: fmxpress_box_side_flyer_45x35.pdf (Infinitely Scalable)
   - High-Res Raster: fmxpress_box_side_300dpi.png (5,315 x 4,134 px, 300 DPI)
   - Standard Web/Digital: fmxpress_box_side_flyer_45x35.png (1,800 x 1,400 px)

3. RECOMMENDED PRINT VENDOR SPECIFICATIONS
-----------------------------------------------------------------------------
- MATERIAL: Heavy-duty outdoor self-adhesive Cast Vinyl (Avery Dennison / 3M IJ180 or equivalent).
- LAMINATION: Gloss or Satin UV-protective overlaminate (weatherproof, waterproof, fuel/rain resistant).
- INK TYPE: Eco-Solvent, Latex, or UV-curable ink for vibrant outdoor longevity.
- APPLICATION: Clean box surface with Isopropyl Alcohol before dry-apply with squeegee.
- BLEED / MARGIN: 10mm safe margin is built-in around all borders.

4. CONTACT & LIVE REPOSITORIES
-----------------------------------------------------------------------------
- Primary WhatsApp Booking: +234 703 785 8093 (0703 785 8093)
- Support Lines: +234 906 795 7295 / +234 903 686 9830
- Official Website: https://fmxpress.tekvolutionhq.com
=============================================================================
"""
with open(spec_path, "w") as f:
    f.write(spec_content)

print("6. Packaging Complete Delivery Box Print Kit ZIP...")
with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(rear_pdf, "01_VECTOR_PDF_PRINT/fmxpress_box_rear_flyer_40x40.pdf")
    z.write(side_pdf, "01_VECTOR_PDF_PRINT/fmxpress_box_side_flyer_45x35.pdf")
    z.write(rear_300dpi, "02_300DPI_HIGH_RES_MASTERS/fmxpress_box_rear_300dpi.png")
    z.write(side_300dpi, "02_300DPI_HIGH_RES_MASTERS/fmxpress_box_side_300dpi.png")
    z.write(rear_png, "03_DIGITAL_PREVIEW/fmxpress_box_rear_flyer_40x40.png")
    z.write(side_png, "03_DIGITAL_PREVIEW/fmxpress_box_side_flyer_45x35.png")
    z.write(f"{workspace_dir}/public/images/fmxpress_box_booking_qr.png", "04_QR_CODE/fmxpress_box_booking_qr.png")
    z.write(spec_path, "README_BOX_PRINT_SPECIFICATIONS.txt")

print(f"-> Generated ZIP Kit: {zip_out} ({os.path.getsize(zip_out):,} bytes)")

# Copy key outputs to brain artifact directory
shutil.copy(rear_png, f"{artifact_dir}/fmxpress_box_rear_flyer_40x40.png")
shutil.copy(side_png, f"{artifact_dir}/fmxpress_box_side_flyer_45x35.png")
shutil.copy(rear_pdf, f"{artifact_dir}/fmxpress_box_rear_flyer_40x40.pdf")
shutil.copy(zip_out, f"{artifact_dir}/FM_XPRESS_Dispatch_Box_Print_Kit.zip")
print("All assets successfully copied to artifacts directory.")
