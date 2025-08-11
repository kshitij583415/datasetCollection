# TextBook Data Collector

This project automates the extraction and conversion of textbook and document files (PDF, DOCX, EPUB, MD) into clean, plain text or markdown for further processing or analysis.

---

## 📁 Directory Structure

- `convert/`  
  Contains conversion scripts (e.g., `converter.py`).
- `scrape/`  
  Contains scraping and cleaning scripts.
- `output/`  
  Stores final merged and cleaned text files.
- `pdf/`, `md/`, `txt/`  
  Store intermediate files by format.
- `requirements.txt`  
  Python dependencies.

---

## ⚙️ How It Works

### 1. **Document Conversion**

The main script for conversion is `convert/converter.py`.  
It supports the following formats:
- **PDF** (`.pdf`)
- **Word** (`.docx`)
- **EPUB** (`.epub`)
- **Markdown** (`.md`)

#### **Conversion Workflow**

1. **PDF Extraction**
   - Tries to extract text using [PyMuPDF (`fitz`)](https://pymupdf.readthedocs.io/).
   - If PyMuPDF fails (e.g., due to PDF errors or advanced features), it falls back to [pdfminer.six](https://pdfminersix.readthedocs.io/).
   - Extracted text is saved as `.txt` or converted to markdown (`.md`).

2. **DOCX Extraction**
   - Reads all paragraphs from the Word document and joins them as plain text.

3. **EPUB Extraction**
   - Extracts document sections from the EPUB, converts them to markdown, and then to plain text.

4. **Markdown to Text**
   - Reads markdown files and saves them as plain text.

5. **Batch Conversion**
   - The function `convert_all_new_pdfs()` processes all PDFs in the `PDF_DIR`, converts them to markdown and then to text, and saves the results in the appropriate directories.

---

### 2. **Text Cleaning and Merging**

- After conversion, the text files can be further cleaned using scripts in the `scrape/` directory.
- Cleaning includes removing unwanted punctuation, references, URLs, and formatting for downstream use.
- Cleaned files are merged into a single output file for analysis or training.

---

## 🏃‍♂️ Usage

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Place your files:**
   - Put PDFs in the `pdf/` directory.
   - DOCX, EPUB, and MD files can be placed as needed.

3. **Run the conversion:**
   ```python
   from convert.converter import convert_all_new_pdfs
   convert_all_new_pdfs()
   ```
   This will process all PDFs and output `.md` and `.txt` files.

4. **(Optional) Run cleaning/merging scripts:**
   - Use scripts in `scrape/` to further clean and merge text files.

---

## 📝 Notes

- If a PDF cannot be processed by PyMuPDF due to advanced features or corruption, the script will automatically try pdfminer.
- Unsupported file formats are skipped.
- All output files are saved in their respective directories.

---

## 📦 Dependencies

- `pymupdf`
- `pdfminer.six`
- `python-docx`
- `ebooklib`
- `markdownify`
- `python-dotenv`
- (See `requirements.txt` for full list)

---

