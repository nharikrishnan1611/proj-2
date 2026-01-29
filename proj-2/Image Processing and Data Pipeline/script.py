import os
import requests
from PIL import Image
from io import BytesIO
import csv
from datetime import datetime

# ==============================
# IMAGE URLS
# ==============================
IMAGE_URLS = [
    "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
]

# ==============================
# REQUEST HEADERS (403 FIX)
# ==============================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ==============================
# CONFIGURATION
# ==============================
IMAGE_DIR = "images"
CSV_FILE = "metadata.csv"
REPORT_FILE = "report.txt"
RESIZE_DIMENSION = (800, 600)
IMAGE_QUALITY = 95

# ==============================
# SETUP
# ==============================
os.makedirs(IMAGE_DIR, exist_ok=True)

with open(CSV_FILE, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Filename",
        "Original Image Size",
        "Final Image Size",
        "Download Timestamp",
        "Source URL"
    ])

success_count = 0

# ==============================
# IMAGE PROCESSING PIPELINE
# ==============================
for index, url in enumerate(IMAGE_URLS, start=1):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        original_size = image.size

        image = image.convert("RGB")
        image = image.resize(RESIZE_DIMENSION)

        filename = f"dragon_{index}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

        image.save(filepath, quality=IMAGE_QUALITY)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                filename,
                original_size,
                image.size,
                timestamp,
                url
            ])

        success_count += 1
        print(f"[SUCCESS] Processed image {index}")

    except Exception as error:
        print(f"[FAILED] Image {index}: {error}")

# ==============================
# REPORT GENERATION
# ==============================
with open(REPORT_FILE, "w") as report:
    report.write("IMAGE PROCESSING & DATA PIPELINE REPORT\n")
    report.write("======================================\n")
    report.write(f"Total URLs provided   : {len(IMAGE_URLS)}\n")
    report.write(f"Images processed      : {success_count}\n")
    report.write(f"Resize dimension      : {RESIZE_DIMENSION[0]} x {RESIZE_DIMENSION[1]}\n")
    report.write(f"Image quality setting : {IMAGE_QUALITY}%\n")
    report.write("Pipeline status       : Completed\n")

print("\nImage Processing and Data Pipeline executed successfully")
print(f"Report generated: {REPORT_FILE}")