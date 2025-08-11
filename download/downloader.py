import os
import requests
from utils.file_utils import ensure_dir, file_exists
from config import PDF_DIR

def download_files(urls):
    ensure_dir(PDF_DIR)
    downloaded = []
    skipped = []
    for url in urls:
        filename = os.path.join(PDF_DIR, os.path.basename(url.split("?")[0]))
        if file_exists(filename):
            print(f"[SKIP] Already downloaded: {filename}")
            skipped.append(filename)
            continue
        try:
            print(f"[DOWNLOAD] {url}")
            r = requests.get(url, stream=True, timeout=15)
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            downloaded.append(filename)
        except Exception as e:
            print(f"[ERROR] Could not download {url}: {e}")
    return downloaded, skipped
