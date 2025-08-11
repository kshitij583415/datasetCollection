# collectors/google_scraper.py
import os, json, hashlib, time
from urllib.parse import urlparse, unquote
import requests
from bs4 import BeautifulSoup
from config import (GOOGLE_API_KEY, GOOGLE_CSE_ID, NUM_RESULTS,
                    DOWNLOAD_DIR, PROCESSED_INDEX, REQUEST_TIMEOUT)

def _load_index():
    if os.path.exists(PROCESSED_INDEX):
        try:
            with open(PROCESSED_INDEX, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_index(idx):
    with open(PROCESSED_INDEX, "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=2)

def _sha256_of_bytes(b):
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def google_search(query, num_results=NUM_RESULTS):
    """
    Use Google Custom Search API if keys exist. Return list of PDF URLs.
    If API keys are not set or API fails, return empty list (caller can fallback to HTML scraping).
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("[INFO] Google API key / CSE not set — skipping Google API.")
        return []

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": min(num_results, 10),
        "fileType": "pdf",
    }
    try:
        r = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        items = data.get("items", [])
        links = []
        for it in items:
            link = it.get("link")
            if link and link.lower().endswith(".pdf"):
                links.append(link)
        print(f"[INFO] Google API returned {len(links)} PDF links for query.")
        return links
    except Exception as e:
        print(f"[WARN] Google API search failed: {e}")
        return []

def html_pdf_links_from_search_page(query, max_links=NUM_RESULTS):
    """
    A simple fallback search: perform a DuckDuckGo HTML search via "https://html.duckduckgo.com/html/" or generic search
    and parse PDF links from result pages (lightweight fallback).
    NOTE: This is basic and may yield duplicates or irrelevant PDFs. Use responsibly.
    """
    base = "https://html.duckduckgo.com/html/"
    try:
        r = requests.post(base, data={"q": query}, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                links.append(href)
                if len(links) >= max_links:
                    break
        print(f"[INFO] Fallback HTML search found {len(links)} PDF links.")
        return links
    except Exception as e:
        print(f"[WARN] HTML fallback search failed: {e}")
        return []

def _filename_from_url(url):
    path = unquote(url.split("?")[0])
    name = os.path.basename(urlparse(path).path)
    if not name:
        name = hashlib.sha1(url.encode("utf-8")).hexdigest() + ".pdf"
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    return name

def download_pdf(url):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    fname = _filename_from_url(url)
    filepath = os.path.join(DOWNLOAD_DIR, fname)

    # If file already exists — compute checksum and still return path (but caller will check processed index)
    if os.path.exists(filepath):
        try:
            with open(filepath, "rb") as f:
                b = f.read()
            checksum = _sha256_of_bytes(b)
            print(f"[SKIP DOWNLOAD] file already exists: {fname} (sha256 {checksum[:8]})")
            return filepath, checksum
        except Exception:
            # fall through to redownload
            pass

    try:
        r = requests.get(url, stream=True, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.content
        checksum = _sha256_of_bytes(data)
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"[DOWNLOADED] {fname} (size: {len(data)} bytes, sha256 {checksum[:8]})")
        return filepath, checksum
    except Exception as e:
        print(f"[ERROR] Failed to download {url}: {e}")
        return None, None

def collect_textbook_pdfs_for_query(query):
    """
    Returns list of downloaded file paths that are NEW (not processed before).
    Index structure: { url: {"sha256":..., "filename":... , "timestamp":... } }
    """
    index = _load_index()
    urls = google_search(query)
    if not urls:
        # fallback to HTML search if google returned nothing
        urls = html_pdf_links_from_search_page(query, max_links=NUM_RESULTS)

    new_downloaded = []
    for url in urls:
        try:
            if url in index:
                print(f"[SKIP] URL already processed: {url}")
                continue
            fp, checksum = download_pdf(url)
            if fp is None:
                continue
            # store in index
            index[url] = {"sha256": checksum, "filename": os.path.basename(fp), "timestamp": int(time.time())}
            new_downloaded.append(fp)
        except Exception as e:
            print(f"[ERROR] processing url {url}: {e}")
            continue

    _save_index(index)
    return new_downloaded
