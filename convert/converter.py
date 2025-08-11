import os
import fitz  # pymupdf
from docx import Document
from ebooklib import epub
from markdownify import markdownify
from utils.file_utils import ensure_dir
from config import DOWNLOAD_DIR, PDF_DIR, MD_DIR, TXT_DIR

def pdf_to_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"[ERROR] fitz failed for {pdf_path}: {e}")
        # Fallback to pdfminer
        try:
            from pdfminer.high_level import extract_text
            return extract_text(pdf_path)
        except Exception as e2:
            print(f"[ERROR] pdfminer also failed for {pdf_path}: {e2}")
            return ""

def docx_to_text(docx_path):
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs])

def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == 9:  # DOCUMENT
            text += markdownify(item.get_content().decode("utf-8"))
    return text

def convert_to_txt(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return file_path
    if ext == ".pdf":
        text = pdf_to_text(file_path)
    elif ext == ".docx":
        text = docx_to_text(file_path)
    elif ext == ".epub":
        text = epub_to_text(file_path)
    else:
        print(f"[SKIP] Unsupported format: {file_path}")
        return None

    txt_path = file_path + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    return txt_path

def pdf_to_md(pdf_path):
    # Use fitz or other lib to extract text, then convert to markdown (use markdownify or similar)
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"[ERROR] fitz failed for {pdf_path}: {e}")
        # Fallback to pdfminer
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(pdf_path)
        except Exception as e2:
            print(f"[ERROR] pdfminer also failed for {pdf_path}: {e2}")
            text = ""
    md_text = markdownify(text)
    md_path = os.path.join(MD_DIR, os.path.splitext(os.path.basename(pdf_path))[0] + ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    return md_path

def md_to_txt(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    txt_path = os.path.join(TXT_DIR, os.path.splitext(os.path.basename(md_path))[0] + ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    return txt_path

def convert_all_new_pdfs():
    ensure_dir(MD_DIR)
    ensure_dir(TXT_DIR)
    pdf_files = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    md_files = []
    txt_files = []
    for pdf in pdf_files:
        md_path = pdf_to_md(pdf)
        md_files.append(md_path)
        txt_path = md_to_txt(md_path)
        txt_files.append(txt_path)
    return txt_files
