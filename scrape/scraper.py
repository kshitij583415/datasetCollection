import os
import re
from utils.file_utils import is_textbook, ensure_dir
from config import OUTPUT_DIR
from utils.index_utils import (
    load_processed_index, 
    save_processed_index, 
    get_file_size_kb,
    print_processed_index_summary  # Add this import
)


# Enhanced exclusion patterns - more comprehensive filtering
EXCLUDE_KEYWORDS = [
    # Document structure
    "appendix", "bibliography", "references", "chapter", "contents", "index",
    "table of contents", "list of figures", "list of tables", "figure", "page", 
    "report", "overview", "document control", "issue", "status", "authority",
    "member agencies", "observer agencies", "section", "publication", "date", 
    "location", "document title", "editorial change", "preface", "foreword",
    "acknowledgment", "dedication", "copyright", "isbn", "issn",
    
    # Navigation elements
    "next page", "previous page", "go to", "click here", "see also",
    "continued on", "end of chapter", "summary", "review questions",
    "exercises", "problems", "solutions", "answers", "glossary",
    
    # Pagination and formatting
    "page number", "header", "footer", "margin", "blank page",
    
    # Version control
    "revision", "version", "draft", "final", "approved", "superseded",
]

# Enhanced regex patterns
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+|ftp://\S+')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
REFERENCE_PATTERN = re.compile(r'\[\d+\]|\(\d+\)|ref\.\s*\d+', re.IGNORECASE)
PAGE_NUM_PATTERN = re.compile(r'^\s*[-]?\s*\d+\s*[-]?\s*$|^\s*page\s+\d+\s*$', re.IGNORECASE)
ROMAN_NUMERAL_PATTERN = re.compile(r'^[ivxlcdm]+\s*$', re.IGNORECASE)
DATE_PATTERN = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b')
TABLE_PATTERN = re.compile(r'table\s+\d+', re.IGNORECASE)
FIGURE_PATTERN = re.compile(r'figure\s+\d+|fig\.\s*\d+', re.IGNORECASE)
DOT_LEADER_PATTERN = re.compile(r'\.{2,}')  # Matches two or more dots (e.g. .. or .....)
EXCESSIVE_SPACES = re.compile(r'\s{3,}')  # Multiple spaces

# NEW: Pattern for multiple consecutive full stops
MULTIPLE_PERIODS = re.compile(r'\.{2,}')  # Two or more consecutive periods
SENTENCE_END_CLEANUP = re.compile(r'\.+\s*\.+')  # Periods separated by spaces

# Patterns for structural elements to completely skip
SKIP_SECTIONS = [
    r'table\s+of\s+contents',
    r'list\s+of\s+(figures|tables|illustrations)',
    r'index\s*$',
    r'bibliography\s*$',
    r'references\s*$',
    r'appendix\s+[a-z]\s*$',
    r'glossary\s*$',
    r'acronyms?\s*$',
    r'abbreviations?\s*$',
]

SKIP_SECTION_PATTERN = re.compile('|'.join(SKIP_SECTIONS), re.IGNORECASE)

def clean_text_basic(text):
    """Basic cleaning - remove URLs, emails, references"""
    text = URL_PATTERN.sub('', text)
    text = EMAIL_PATTERN.sub('', text)
    text = REFERENCE_PATTERN.sub('', text)
    text = DATE_PATTERN.sub('', text)
    text = DOT_LEADER_PATTERN.sub('.', text)
    text = EXCESSIVE_SPACES.sub(' ', text)
    return text

def normalize_sentence_endings(text):
    """Fix multiple full stops and ensure proper sentence endings"""
    # Replace multiple consecutive periods with single period
    text = MULTIPLE_PERIODS.sub('.', text)
    
    # Fix periods separated by spaces (e.g., ". . ." -> ".")
    text = SENTENCE_END_CLEANUP.sub('.', text)
    
    # Fix common issues with sentence endings
    text = re.sub(r'\.\s*\.\s*\.', '.', text)  # Three periods with spaces
    text = re.sub(r'\.+\s+\.+', '. ', text)    # Multiple periods across spaces
    
    # Ensure single space after periods (sentence separation)
    text = re.sub(r'\.(\s{0,1})([A-Z])', r'. \2', text)  # Period followed by capital letter
    text = re.sub(r'\.(\s{2,})', r'. ', text)             # Period followed by multiple spaces
    
    # Handle edge cases where periods might be at end of lines
    text = re.sub(r'\.\s*\n\s*\.', '.\n', text)
    
    return text

def is_table_of_contents_line(line):
    """Detect table of contents entries"""
    stripped = line.strip()
    
    # Lines with dots followed by numbers (typical TOC format)
    if re.search(r'\.{2,}\s*\d+\s*$', stripped):
        return True
    
    # Lines ending with just numbers (page references)
    if re.search(r'\s+\d+\s*$', stripped) and len(stripped.split()) > 1:
        return True
    
    # Lines with chapter/section numbers followed by titles
    if re.search(r'^\s*\d+(\.\d+)*\s+[A-Z]', stripped):
        return True
        
    return False

def is_header_footer(line):
    """Detect headers and footers"""
    stripped = line.strip()
    
    # Very short lines at start/end are likely headers/footers
    if len(stripped) < 10:
        return True
    
    # Lines with just uppercase words (headers)
    words = stripped.split()
    if len(words) <= 4 and all(word.isupper() or word.isdigit() for word in words):
        return True
    
    return False

def is_excluded_line(line):
    """Enhanced line filtering"""
    stripped = line.strip().lower()
    
    # Empty lines are kept for paragraph breaks
    if not stripped:
        return False
    
    # Skip very short lines (likely formatting artifacts)
    if len(stripped) <= 2:
        return True
    
    # Skip page numbers and roman numerals
    if PAGE_NUM_PATTERN.match(stripped) or ROMAN_NUMERAL_PATTERN.match(stripped):
        return True
    
    # Skip table/figure references
    if TABLE_PATTERN.search(stripped) or FIGURE_PATTERN.search(stripped):
        return True
    
    # Skip TOC entries
    if is_table_of_contents_line(line):
        return True
    
    # Skip headers/footers
    if is_header_footer(line):
        return True
    
    # Skip lines with excluded keywords
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in stripped:
            return True
    
    # Skip lines that are mostly numbers and special characters
    alpha_chars = sum(1 for c in stripped if c.isalpha())
    if len(stripped) > 3 and alpha_chars / len(stripped) < 0.3:
        return True
    
    # Skip lines with excessive punctuation (likely formatting)
    punct_count = sum(1 for c in stripped if c in '.,;:!?-_=+[]{}()|\\/')
    if punct_count > len(stripped) * 0.5:
        return True
    
    return False

def extract_meaningful_content(lines):
    """Extract only meaningful content paragraphs"""
    meaningful_lines = []
    skip_section = False
    skip_count = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check if we're entering a section to skip entirely
        if SKIP_SECTION_PATTERN.search(stripped):
            skip_section = True
            skip_count = 0
            continue
        
        # Stop skipping after several empty lines or clear content start
        if skip_section:
            if not stripped:
                skip_count += 1
                if skip_count > 2:  # After 2 empty lines, assume section ended
                    skip_section = False
                continue
            else:
                skip_count = 0
                # Look ahead to see if this looks like real content
                if len(stripped) > 20 and not is_excluded_line(line):
                    skip_section = False
                else:
                    continue
        
        if is_excluded_line(line):
            continue
        
        # Only keep lines with substantial content
        if len(stripped) > 15:  # Minimum meaningful content length
            meaningful_lines.append(stripped)
    
    return meaningful_lines

def form_paragraphs(lines):
    """Form coherent paragraphs from cleaned lines"""
    paragraphs = []
    current_paragraph = []
    
    for line in lines:
        # Start new paragraph if line starts with capital or after empty line
        if (current_paragraph and 
            (line[0].isupper() and not current_paragraph[-1].endswith('.')) or
            len(line) < 50):  # Short lines might be new topics
            
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        
        current_paragraph.append(line)
        
        # End paragraph if line ends with period and next conditions
        if line.endswith('.') and len(current_paragraph) > 1:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
    
    # Don't forget the last paragraph
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    return paragraphs

def clean_content(text):
    """Main cleaning function with enhanced filtering and full stop normalization"""
    # Basic text cleaning
    text = clean_text_basic(text)
    
    lines = text.splitlines()
    
    # Extract meaningful content
    meaningful_lines = extract_meaningful_content(lines)
    
    # Form paragraphs
    paragraphs = form_paragraphs(meaningful_lines)
    
    # Filter paragraphs by quality
    quality_paragraphs = []
    for para in paragraphs:
        # Skip very short paragraphs
        if len(para) < 50:
            continue
        
        # Skip paragraphs with too many numbers (likely data tables)
        word_count = len(para.split())
        number_count = len(re.findall(r'\b\d+\b', para))
        if number_count > word_count * 0.3:
            continue
        
        # Skip paragraphs that are mostly uppercase (likely headers)
        if sum(1 for c in para if c.isupper()) > len(para) * 0.5:
            continue
        
        quality_paragraphs.append(para)
    
    # Join paragraphs
    cleaned_text = '\n\n'.join(quality_paragraphs)
    
    # Remove brackets and their contents (e.g., [1], (see Fig. 2), etc.)
    cleaned_text = re.sub(r'\[[^\]]*\]', '', cleaned_text)
    cleaned_text = re.sub(r'\([^\)]*\)', '', cleaned_text)

    # Remove most punctuation except periods (optional: keep only a-z, A-Z, 0-9, and .)
    cleaned_text = re.sub(r'[^\w\s\.]', '', cleaned_text)

    # Remove isolated single letters (often list markers)
    cleaned_text = re.sub(r'\b[a-zA-Z]\b', '', cleaned_text)

    # IMPORTANT: Normalize sentence endings BEFORE final cleanup
    cleaned_text = normalize_sentence_endings(cleaned_text)
    
    # Final cleanup
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    return cleaned_text.strip()

def validate_content_quality(content):
    """Check if the cleaned content is of good quality for chatbot training"""
    if len(content) < 500:  # Too short
        return False
    
    # Check ratio of alphabetic characters
    alpha_ratio = sum(1 for c in content if c.isalpha()) / len(content)
    if alpha_ratio < 0.6:  # Less than 60% alphabetic characters
        return False
    
    # Check for reasonable sentence structure
    sentences = re.split(r'[.!?]+', content)
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
    if avg_sentence_length < 5 or avg_sentence_length > 100:  # Too short or too long
        return False
    
    return True

# def scrape_and_merge(txt_files, output_name):
#     """Enhanced scraping and merging with quality validation"""
#     ensure_dir(OUTPUT_DIR)
#     processed_set = load_processed_index()
#     merged_content = ""
#     processed_count = 0
#     skipped_count = 0

#     output_path = os.path.join(OUTPUT_DIR, "final_mergedFile.txt")
#     append_mode = os.path.exists(output_path)

#     for txt_file in txt_files:
#         if txt_file in processed_set:
#             print(f"[SKIP] Already processed: {txt_file}")
#             continue
#         try:
#             with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
#                 content = f.read()
#                 if not is_textbook(content):
#                     print(f"[SKIP] Not a textbook: {txt_file}")
#                     skipped_count += 1
#                     continue
#                 cleaned_content = clean_content(content)
#                 if not validate_content_quality(cleaned_content):
#                     print(f"[SKIP] Low quality content: {txt_file}")
#                     skipped_count += 1
#                     continue
#                 print(f"[PROCESS] Adding {txt_file} ({len(cleaned_content)} chars)")
#                 merged_content += "\n\n" + cleaned_content
#                 processed_set.add(txt_file)
#                 processed_count += 1
#         except Exception as e:
#             print(f"[ERROR] Reading {txt_file}: {e}")
#             skipped_count += 1

#     if merged_content:
#         with open(output_path, "a" if append_mode else "w", encoding="utf-8") as f:
#             f.write(merged_content.strip() + "\n")
#         print(f"Updated file: {output_path}")
#     else:
#         print("No new content to add.")

#     save_processed_index(processed_set)
#     print(f"[DONE] Processed: {processed_count}, Skipped: {skipped_count}")
#     print(f"[DONE] Merged file saved: {output_path}")

#     return merged_content


def scrape_and_merge(txt_files, output_name, file_metadata=None):
    """Enhanced scraping and merging with detailed metadata tracking
    
    Args:
        txt_files: List of text files to process
        output_name: Name for output file
        file_metadata: Dict mapping file_path to {'title': str, 'pdf_url': str}
    """
    ensure_dir(OUTPUT_DIR)
    processed_dict, processed_set = load_processed_index()
    merged_content = ""
    processed_count = 0
    skipped_count = 0

    output_path = os.path.join(OUTPUT_DIR, "final_mergedFile.txt")
    append_mode = os.path.exists(output_path)

    for txt_file in txt_files:
        if txt_file in processed_set:
            print(f"[SKIP] Already processed: {txt_file}")
            continue
            
        try:
            with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
                if not is_textbook(content):
                    print(f"[SKIP] Not a textbook: {txt_file}")
                    skipped_count += 1
                    continue
                    
                cleaned_content = clean_content(content)
                
                if not validate_content_quality(cleaned_content):
                    print(f"[SKIP] Low quality content: {txt_file}")
                    skipped_count += 1
                    continue
                
                # Get file metadata
                file_size_kb = get_file_size_kb(txt_file)
                metadata = file_metadata.get(txt_file, {}) if file_metadata else {}
                title = metadata.get('title', 'Unknown')
                pdf_url = metadata.get('pdf_url', 'Unknown')
                
                print(f"[PROCESS] Adding {txt_file} ({len(cleaned_content)} chars)")
                print(f"          Title: {title[:50]}...")
                print(f"          Size: {file_size_kb} KB")
                
                merged_content += "\n\n" + cleaned_content
                
                # Add to processed index with full metadata
                processed_dict[txt_file] = {
                    'title': title,
                    'pdf_url': pdf_url,
                    'file_size_kb': file_size_kb
                }
                processed_count += 1
                
        except Exception as e:
            print(f"[ERROR] Reading {txt_file}: {e}")
            skipped_count += 1

    # Save updated index
    if processed_count > 0:
        save_processed_index(processed_dict)

    # Save merged content
    if merged_content:
        with open(output_path, "a" if append_mode else "w", encoding="utf-8") as f:
            f.write(merged_content.strip() + "\n")
        print(f"Updated file: {output_path}")
    else:
        print("No new content to add.")

    print(f"[DONE] Processed: {processed_count}, Skipped: {skipped_count}")
    print(f"[DONE] Merged file saved: {output_path}")
    
    # Print summary
    print_processed_index_summary()

    return merged_content

# Example usage function
def process_files_with_metadata(txt_files, metadata_source=None):
    """Process files with metadata from various sources
    
    Args:
        txt_files: List of text file paths
        metadata_source: Can be:
            - dict: Direct mapping of file_path -> {'title': str, 'pdf_url': str}
            - str: Path to CSV file with columns: File_Path, Title, pdf_url
            - None: Extract metadata from filename/path
    """
    
    file_metadata = {}
    
    if isinstance(metadata_source, dict):
        file_metadata = metadata_source
    elif isinstance(metadata_source, str) and os.path.exists(metadata_source):
        # Load from CSV file
        try:
            with open(metadata_source, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    file_path = row.get('File_Path', '')
                    if file_path:
                        file_metadata[file_path] = {
                            'title': row.get('Title', 'Unknown'),
                            'pdf_url': row.get('pdf_url', 'Unknown')
                        }
        except Exception as e:
            print(f"Error loading metadata from CSV: {e}")
    else:
        # Extract from filename
        for txt_file in txt_files:
            filename = os.path.basename(txt_file)
            title = filename.replace('.txt', '').replace('_', ' ').title()
            file_metadata[txt_file] = {
                'title': title,
                'pdf_url': 'Unknown'
            }
    
    return scrape_and_merge(txt_files, "merged_output", file_metadata)