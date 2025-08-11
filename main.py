# # from googleapiclient.errors import HttpError
# # from search.google_search import search_textbooks
# # from download.downloader import download_files
# # from convert.converter import convert_to_txt, convert_all_new_pdfs
# # from scrape.scraper import scrape_and_merge
# # from search.search_itut import search_itut_papers
# # from utils.file_utils import list_files
# # from config import DOWNLOAD_DIR, TXT_DIR
# # import os

# # def main():
# #     topic = input("Enter topic: ").strip()
# #     layer = input("Enter layer (L1, L2, L3): ").strip()
    
# #     # Construct queries
# #     textbook_query = f"{topic} {layer} protocol textbook filetype:pdf OR filetype:docx OR filetype:txt OR filetype:epub"
# #     # itut_query = f"{topic} {layer} protocol"

# #     # Step 1: Search
# #     try:
# #         print("\n[SEARCH] Searching for textbooks...")
# #         textbook_urls = search_textbooks(textbook_query)
# #         print(f"Found {len(textbook_urls)} textbook URLs.")

# #         # print("\n[SEARCH] Searching for ITU-T papers...")
# #         # itut_urls = search_itut_papers(itut_query)
# #         # print(f"Found {len(itut_urls)} ITU-T paper URLs.")

# #         # # Combine and deduplicate URLs
# #         # all_urls = list(set(textbook_urls + itut_urls))
# #         # print(f"\nFound {len(all_urls)} unique URLs in total.")
# #     except HttpError as e:
# #         print(f"\n[ERROR] An error occurred with the Google Search API: {e}")
# #         print("\nPlease ensure the following:")
# #         print("1. Your GOOGLE_API_KEY and GOOGLE_CSE_ID in the .env file are correct.")
# #         print("2. The Custom Search API is enabled in your Google Cloud project.")
# #         print("3. Your account has not exceeded its daily query limit.")
# #         return

# #     # Step 2: Download
# #     if not textbook_urls:
# #         print("\n[INFO] No new URLs to download. Exiting.")
# #         return
        
# #     print("\n[DOWNLOAD] Starting download...")
# #     downloaded, skipped = download_files(textbook_urls)
    
# #     # Step 3: Convert new PDFs to MD and then to TXT
# #     print("\n[CONVERT] Converting PDFs to MD and then to TXT...")
# #     txt_files = convert_all_new_pdfs()

# #     # Step 4: Scrape & Merge only new TXT files
# #     print("\n[SCRAPE] Extracting and merging...")
# #     all_txt_files = [os.path.join(TXT_DIR, f) for f in os.listdir(TXT_DIR) if f.endswith(".txt")]
# #     if all_txt_files:
# #         scrape_and_merge(all_txt_files, "final_mergedFile")
# #     else:
# #         print("\n[INFO] No text files to scrape and merge.")

# # if __name__ == "__main__":
# #     main()


# from googleapiclient.errors import HttpError
# from search.google_search import search_textbooks
# from download.downloader import download_files
# from convert.converter import convert_to_txt, convert_all_new_pdfs
# from scrape.scraper import scrape_and_merge
# from search.search_itut import search_itut_papers
# from utils.file_utils import list_files
# from utils.textbook_metadata import extract_textbook_metadata
# from config import DOWNLOAD_DIR, TXT_DIR
# import os

# def main():
#     topic = input("Enter topic: ").strip()
#     layer = input("Enter layer (L1, L2, L3): ").strip()
    
#     # Construct queries
#     textbook_query = f"{topic} {layer} protocol textbook filetype:pdf OR filetype:docx OR filetype:txt OR filetype:epub"
#     # itut_query = f"{topic} {layer} protocol"

#     # Step 1: Search for textbooks
#     textbook_urls = []
#     try:
#         print("\n[SEARCH] Searching for textbooks...")
#         textbook_urls = search_textbooks(textbook_query)
#         print(f"Found {len(textbook_urls)} textbook URLs.")
#     except HttpError as e:
#         print(f"\n[ERROR] An error occurred with the Google Search API: {e}")
#         print("\nPlease ensure the following:")
#         print("1. Your GOOGLE_API_KEY and GOOGLE_CSE_ID in the .env file are correct.")
#         print("2. The Custom Search API is enabled in your Google Cloud project.")
#         print("3. Your account has not exceeded its daily query limit.")
#         return

#     # Step 2: Search for ITU-T papers (separate handling)
#     # itut_urls = []
#     # try:
#     #     print("\n[SEARCH] Searching for ITU-T papers...")
#     #     itut_urls = search_itut_papers(itut_query)
#     #     print(f"Found {len(itut_urls)} ITU-T paper URLs.")
#     # except Exception as e:
#     #     print(f"\n[WARNING] ITU-T search failed: {e}")

#     # Combine URLs but keep track of sources
#     all_urls = textbook_urls
#     print(f"\nFound {len(all_urls)} total URLs ({len(textbook_urls)}")

#     if not all_urls:
#         print("\n[INFO] No URLs found. Exiting.")
#         return

#     # Step 3: Download files
#     print("\n[DOWNLOAD] Starting download...")
#     downloaded, skipped = download_files(all_urls)
#     print(f"Downloaded: {downloaded}, Skipped: {skipped}")

#     # Step 4: Convert PDFs to TXT
#     print("\n[CONVERT] Converting PDFs to MD and then to TXT...")
#     txt_files = convert_all_new_pdfs()

#     # Step 5: Extract metadata for textbooks only (ITU-T papers handled separately)
#     print("\n[METADATA] Extracting textbook metadata...")
#     all_txt_files = [os.path.join(TXT_DIR, f) for f in os.listdir(TXT_DIR) if f.endswith(".txt")]
    
#     if all_txt_files:
#         # Extract metadata primarily from textbook URLs
#         # For ITU-T papers, we'll use a simpler approach since they have different patterns
#         textbook_metadata = extract_textbook_metadata(textbook_urls, all_txt_files, DOWNLOAD_DIR)
        
#         # Handle ITU-T papers separately if needed
#         # itut_metadata = extract_itut_metadata(itut_urls, all_txt_files, DOWNLOAD_DIR)
        
#         # Combine metadata
#         combined_metadata = {**textbook_metadata}
        
#         print(f"\nExtracted metadata for {len(combined_metadata)} files:")
#         print(f"  - Textbooks: {len(textbook_metadata)}")
#         # print(f"  - ITU-T papers: {len(itut_metadata)}")
        
#         # Preview metadata
#         print("\n--- Metadata Preview ---")
#         for i, (file_path, metadata) in enumerate(list(combined_metadata.items())[:3]):
#             print(f"{i+1}. File: {os.path.basename(file_path)}")
#             print(f"   Title: {metadata['title']}")
#             print(f"   URL: {metadata['pdf_url'][:80]}...")
#             print()

#         # Step 6: Scrape & Merge with metadata
#         print("\n[SCRAPE] Extracting and merging with metadata...")
#         scrape_and_merge(all_txt_files, "final_mergedFile", combined_metadata)
#     else:
#         print("\n[INFO] No text files to scrape and merge.")

# # def extract_itut_metadata(itut_urls, txt_files, download_dir):
# #     """
# #     Extract metadata for ITU-T papers (simpler approach since they follow different patterns).
# #     """
# #     # This is a simplified version for ITU-T papers
# #     # You can expand this based on ITU-T specific patterns
    
# #     itut_metadata = {}
    
# #     # For now, just handle files that couldn't be matched by textbook extractor
# #     # In a full implementation, you'd have ITU-T specific pattern matching
    
# #     for txt_file in txt_files:
# #         # Skip if already handled by textbook metadata
# #         if any(txt_file in metadata for metadata in [{}]):  # This would be filled by actual logic
# #             continue
            
# #         filename = os.path.basename(txt_file)
# #         name_without_ext = os.path.splitext(filename)[0]
        
# #         # ITU-T specific patterns
# #         if any(pattern in name_without_ext.lower() for pattern in ['itu', 'g.', 'h.', 'x.', 'y.', 'recommendation']):
# #             title = f"ITU-T Recommendation - {name_without_ext.replace('_', ' ').title()}"
# #             # Try to find matching URL
# #             matching_url = find_matching_itut_url(name_without_ext, itut_urls)
# #             itut_metadata[txt_file] = {
# #                 'title': title,
# #                 'pdf_url': matching_url or f"ITU-T_Source_{filename}"
# #             }
    
# #     return itut_metadata

# # def find_matching_itut_url(filename_part, itut_urls):
# #     """Find matching ITU-T URL for a filename."""
# #     filename_words = set(filename_part.lower().split())
    
# #     for url in itut_urls:
# #         url_words = set(url.lower().split())
# #         # Simple word overlap matching
# #         if len(filename_words.intersection(url_words)) > 0:
# #             return url
    
# #     return None

# if __name__ == "__main__":
#     main()


from googleapiclient.errors import HttpError
from search.google_search import search_textbooks
from download.downloader import download_files
from convert.converter import convert_to_txt, convert_all_new_pdfs
from scrape.scraper import scrape_and_merge
from utils.textbook_metadata import extract_textbook_metadata
from config import DOWNLOAD_DIR, TXT_DIR
import os

def main():
    topic = input("Enter topic: ").strip()
    layer = input("Enter layer (L1, L2, L3): ").strip()
    
    # Construct query
    textbook_query = f"{topic} {layer} protocol textbook filetype:pdf OR filetype:docx OR filetype:txt OR filetype:epub"
    
    # Step 1: Search for textbooks
    textbook_urls = []
    try:
        print("\n[SEARCH] Searching for textbooks...")
        textbook_urls = search_textbooks(textbook_query)
        print(f"Found {len(textbook_urls)} textbook URLs.")
    except HttpError as e:
        print(f"\n[ERROR] An error occurred with the Google Search API: {e}")
        print("\nPlease ensure the following:")
        print("1. Your GOOGLE_API_KEY and GOOGLE_CSE_ID in the .env file are correct.")
        print("2. The Custom Search API is enabled in your Google Cloud project.")
        print("3. Your account has not exceeded its daily query limit.")
        return

    if not textbook_urls:
        print("\n[INFO] No textbook URLs found. Exiting.")
        return

    # Step 2: Download files
    print("\n[DOWNLOAD] Starting download...")
    downloaded, skipped = download_files(textbook_urls)
    print(f"Downloaded: {downloaded}, Skipped: {skipped}")

    # Step 3: Convert new PDFs to TXT
    print("\n[CONVERT] Converting PDFs to MD and then to TXT...")
    txt_files = convert_all_new_pdfs()

    # Step 4: Extract metadata
    all_txt_files = [os.path.join(TXT_DIR, f) for f in os.listdir(TXT_DIR) if f.endswith(".txt")]
    
    # IMPORTANT: Pass the correct PDF download directory (usually downloads/pdfs)
    pdf_dir = os.path.join(DOWNLOAD_DIR, "pdfs")
    
    print("\n[METADATA] Extracting textbook metadata...")
    if all_txt_files:
        textbook_metadata = extract_textbook_metadata(textbook_urls, all_txt_files, pdf_dir)
        
        print(f"\nExtracted metadata for {len(textbook_metadata)} files.")
        
        print("\n[SCRAPE] Extracting and merging with metadata...")
        scrape_and_merge(all_txt_files, "final_mergedFile", textbook_metadata)
    else:
        print("\n[INFO] No text files to scrape and merge.")

if __name__ == "__main__":
    main()
