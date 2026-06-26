import os
import time
import sys
import random
import json
from compress_pdf import compress_pdf

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


MAX_SIZE = 10 * 1024 * 1024  # 10 MB

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <input_dir>")
    sys.exit(1)

INPUT_DIR = sys.argv[1]

if not os.path.isdir(INPUT_DIR):
    print(f"Error: '{INPUT_DIR}' is not a valid directory.")
    sys.exit(1)

OUTPUT_DIR = os.path.abspath(os.path.join(INPUT_DIR, "translated"))
print(f"Output directory: {OUTPUT_DIR}")
os.makedirs(OUTPUT_DIR, exist_ok=True)


prefs = {
    "download.default_directory": OUTPUT_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
}

options = webdriver.ChromeOptions()

# Hide the browser window
options.add_argument("--disable-gpu")
options.add_argument("--window-position=-2000,0")
options.add_argument("--window-size=1280,720")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=en-US")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.execute_script("""
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
""")

wait = WebDriverWait(driver, 60)

URL = "https://translate.google.com/?sl=en&tl=vi&op=docs"

files = sorted(os.listdir(INPUT_DIR))
files = [f for f in files if f.endswith(".pdf")]

for file in files:
    print("=" * 60)
    print(f"Processing file: {file}")

    driver.get(URL)

    # chờ trang load
    upload = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type=file]"))
    )
    upload_file = compress_pdf(
        os.path.join(INPUT_DIR, file), max_size=MAX_SIZE, tail="_vi"
    )
    if os.path.getsize(upload_file) > MAX_SIZE:
        print(
            f"Warning: {os.path.basename(upload_file)}: {os.path.getsize(upload_file) / 1024 / 1024:.2f} is still larger than {MAX_SIZE / 1024 / 1024:.2f} MB"
        )
        continue

    upload.send_keys(upload_file)

    print("Upload file:", os.path.basename(upload_file))

    # đợi nút Translate
    try:
        translate_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(),'Translate')]]")
            )
        )
        time.sleep(random.random())

        translate_btn.click()

    except:
        print("Translate button not found.")
        print("Skipping file:", os.path.basename(upload_file))
        continue

    print("Translating...")

    # chờ nút Download
    try:
        download_btn = WebDriverWait(driver, 600).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(),'Download translation')]]")
            )
        )

        base, ext = os.path.splitext(os.path.basename(upload_file))
        download_file = os.path.join(OUTPUT_DIR, f"{base}{ext}")
        i = 1

        while os.path.exists(download_file):
            download_file = os.path.join(OUTPUT_DIR, f"{base} ({i}){ext}")
            i += 1
        print(f"Downloading to: {download_file}")
        time.sleep(random.random())

        download_btn.click()

        WebDriverWait(driver, 600).until(
            lambda d: (
                os.path.exists(download_file) and os.path.getsize(download_file) > 0
            )
        )

        print(
            f"Downloaded  {os.path.basename(download_file)} ({os.path.getsize(download_file) / 1024 / 1024:.2f} MB)"
        )

    except:
        print("Download button not found.")
        print("Skipping file:", os.path.basename(upload_file))
        continue
    time.sleep(random.random())

driver.quit()


# remove compressed files
compressed_dir = os.path.join(INPUT_DIR, "compressed")
if os.path.exists(compressed_dir):
    for f in os.listdir(compressed_dir):
        os.remove(os.path.join(compressed_dir, f))
    os.rmdir(compressed_dir)

print("Done.")
