import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

DOWNLOAD_DIR = "downloads"
PDF_DIR = os.path.join(DOWNLOAD_DIR, "pdfs")
MD_DIR = os.path.join(DOWNLOAD_DIR, "mds")
TXT_DIR = os.path.join(DOWNLOAD_DIR, "txts")
OUTPUT_DIR = "output"
PROCESSED_INDEX = "processed_index.csv"

TEXTBOOK_KEYWORDS = ["chapter", "contents", "lesson", "exercise", "unit",
                     "introduction", "preface", "glossary", "appendix", "references", "bibliography"]

NUM_RESULTS = 10
REQUEST_TIMEOUT = 15
