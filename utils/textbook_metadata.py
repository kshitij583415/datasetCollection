# import os
# import urllib.parse
# import re
# from typing import Dict, List, Optional
# import json

# class TextbookMetadataExtractor:
#     """Extract and map textbook metadata from URLs and downloaded files."""

#     def __init__(self):
#         self.url_to_metadata = {}
#         self.file_to_metadata = {}

#     def extract_textbook_info_from_url(self, url: str) -> Dict[str, str]:
#         try:
#             parsed_url = urllib.parse.urlparse(url)
#             filename = os.path.basename(parsed_url.path) or "textbook"
#             name_without_ext = os.path.splitext(filename)[0]
#             decoded_name = urllib.parse.unquote(name_without_ext)
#             title = self._extract_title_from_decoded_name(decoded_name)

#             return {
#                 'title': title,
#                 'clean_url': url,
#                 'filename': filename
#             }
#         except Exception as e:
#             print(f"Error extracting info from URL {url}: {e}")
#             return {
#                 'title': 'Unknown Textbook',
#                 'clean_url': url,
#                 'filename': 'unknown'
#             }

#     def _extract_title_from_decoded_name(self, decoded_name: str) -> str:
#         clean_name = decoded_name.replace('_', ' ').replace('-', ' ').replace('%20', ' ')
#         clean_name = re.sub(r'\s+', ' ', clean_name).strip()
#         return clean_name.title() if clean_name else "Unknown Textbook"

#     def store_url_metadata(self, urls: List[str]) -> Dict[str, Dict[str, str]]:
#         url_metadata = {}
#         for url in urls:
#             metadata = self.extract_textbook_info_from_url(url)
#             url_metadata[url] = metadata
#             self.url_to_metadata[url] = metadata
#         return url_metadata

#     def map_files_to_urls(self, txt_files: List[str], downloaded_files: List[str]) -> Dict[str, Dict[str, str]]:
#         file_metadata = {}
#         downloaded_to_url = self._match_downloaded_files_to_urls(downloaded_files)

#         for txt_file in txt_files:
#             txt_basename = os.path.basename(txt_file)
#             txt_name = os.path.splitext(txt_basename)[0]

#             best_match_url = None
#             best_match_metadata = None
#             best_score = 0

#             print(f"\nMatching TXT file '{txt_basename}'...")

#             for downloaded_file, url in downloaded_to_url.items():
#                 downloaded_basename = os.path.basename(downloaded_file)
#                 downloaded_name = os.path.splitext(downloaded_basename)[0]

#                 score = self._calculate_name_similarity(txt_name, downloaded_name)
#                 print(f"  Compared to downloaded '{downloaded_basename}', similarity score: {score:.3f}")

#                 if score > best_score and score > 0.3:
#                     best_score = score
#                     best_match_url = url
#                     best_match_metadata = self.url_to_metadata.get(url)

#             if best_match_metadata:
#                 file_metadata[txt_file] = {
#                     'title': best_match_metadata['title'],
#                     'pdf_url': best_match_url
#                 }
#                 print(f"  --> Matched URL: {best_match_url}")
#             else:
#                 fallback_title = self._extract_title_from_decoded_name(txt_name)
#                 file_metadata[txt_file] = {
#                     'title': fallback_title,
#                     'pdf_url': f"Local_File_{txt_basename}"
#                 }
#                 print(f"  --> No good match found. Using fallback.")

#         self.file_to_metadata = file_metadata
#         return file_metadata

#     def _match_downloaded_files_to_urls(self, downloaded_files: List[str]) -> Dict[str, str]:
#         downloaded_to_url = {}

#         for downloaded_file in downloaded_files:
#             downloaded_basename = os.path.basename(downloaded_file)
#             downloaded_name = os.path.splitext(downloaded_basename)[0]

#             best_match_url = None
#             best_score = 0

#             for url, metadata in self.url_to_metadata.items():
#                 url_filename = metadata.get('filename', '')
#                 url_name = os.path.splitext(url_filename)[0]

#                 score = self._calculate_name_similarity(downloaded_name, url_name)

#                 if score > best_score and score > 0.3:
#                     best_score = score
#                     best_match_url = url

#             if best_match_url:
#                 downloaded_to_url[downloaded_file] = best_match_url
#                 print(f"Matched downloaded file '{downloaded_basename}' to URL: {best_match_url}")
#             else:
#                 print(f"No URL match for downloaded file '{downloaded_basename}'")

#         return downloaded_to_url

#     def _calculate_name_similarity(self, name1: str, name2: str) -> float:
#         norm1 = self._normalize_filename(name1)
#         norm2 = self._normalize_filename(name2)

#         if norm1 == norm2:
#             return 1.0
#         if norm1 in norm2 or norm2 in norm1:
#             return 0.8

#         words1 = set(re.findall(r'\w+', norm1.lower()))
#         words2 = set(re.findall(r'\w+', norm2.lower()))

#         if not words1 or not words2:
#             return 0.0

#         intersection = words1.intersection(words2)
#         union = words1.union(words2)
#         return len(intersection) / len(union) if union else 0.0

#     def _normalize_filename(self, filename: str) -> str:
#         normalized = urllib.parse.unquote(filename)
#         normalized = re.sub(r'[_\-\s%20]+', ' ', normalized)
#         normalized = re.sub(r'\s+', ' ', normalized).strip().lower()
#         return normalized

#     def save_metadata_to_json(self, filepath: str = "textbook_metadata.json"):
#         data = {
#             'url_to_metadata': self.url_to_metadata,
#             'file_to_metadata': self.file_to_metadata
#         }
#         try:
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 json.dump(data, f, indent=2, ensure_ascii=False)
#             print(f"Metadata saved to {filepath}")
#         except Exception as e:
#             print(f"Error saving metadata: {e}")

#     def load_metadata_from_json(self, filepath: str = "textbook_metadata.json"):
#         try:
#             if os.path.exists(filepath):
#                 with open(filepath, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                 self.url_to_metadata = data.get('url_to_metadata', {})
#                 self.file_to_metadata = data.get('file_to_metadata', {})
#                 print(f"Metadata loaded from {filepath}")
#         except Exception as e:
#             print(f"Error loading metadata: {e}")

#     def get_file_metadata(self, file_path: str) -> Optional[Dict[str, str]]:
#         return self.file_to_metadata.get(file_path)

#     def print_summary(self):
#         print(f"\n=== Textbook Metadata Summary ===")
#         print(f"URLs processed: {len(self.url_to_metadata)}")
#         print(f"Files mapped: {len(self.file_to_metadata)}")

#         print("\n--- URL Metadata ---")
#         for i, (url, metadata) in enumerate(list(self.url_to_metadata.items())[:3]):
#             print(f"{i+1}. URL: {url[:60]}...")
#             print(f"   Title: {metadata['title']}\n")

#         print("\n--- File Metadata ---")
#         for i, (file_path, metadata) in enumerate(list(self.file_to_metadata.items())[:3]):
#             print(f"{i+1}. File: {os.path.basename(file_path)}")
#             print(f"   Title: {metadata['title']}")
#             print(f"   URL: {metadata['pdf_url'][:60]}...\n")

# def extract_textbook_metadata(search_urls: List[str], txt_files: List[str], download_dir: str) -> Dict[str, Dict[str, str]]:
#     extractor = TextbookMetadataExtractor()
#     extractor.store_url_metadata(search_urls)

#     downloaded_files = []
#     if os.path.exists(download_dir):
#         for f in os.listdir(download_dir):
#             if not f.startswith('.'):
#                 downloaded_files.append(os.path.join(download_dir, f))

#     file_metadata = extractor.map_files_to_urls(txt_files, downloaded_files)
#     extractor.print_summary()
#     return file_metadata


import os
import urllib.parse
import re
from typing import Dict, List, Optional
import json

class TextbookMetadataExtractor:
    def __init__(self):
        self.url_to_metadata = {}
        self.file_to_metadata = {}

    def extract_textbook_info_from_url(self, url: str) -> Dict[str, str]:
        try:
            parsed_url = urllib.parse.urlparse(url)
            path = parsed_url.path
            filename = os.path.basename(path)
            if not filename:
                filename = "textbook"
            name_without_ext = os.path.splitext(filename)[0]
            decoded_name = urllib.parse.unquote(name_without_ext)
            title = self._extract_title_from_decoded_name(decoded_name, url)
            return {
                'title': title,
                'clean_url': url,
                'filename': filename
            }
        except Exception as e:
            print(f"Error extracting info from URL {url}: {e}")
            return {
                'title': 'Unknown Textbook',
                'clean_url': url,
                'filename': 'unknown'
            }

    def _extract_title_from_decoded_name(self, decoded_name: str, url: str) -> str:
        clean_name = decoded_name.replace('_', ' ').replace('-', ' ').replace('%20', ' ')
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()

        author_patterns = {
            'tanenbaum': 'Computer Networks by Andrew S. Tanenbaum',
            'kurose': 'Computer Networking: A Top-Down Approach by Kurose & Ross',
            'stallings': 'Data and Computer Communications by William Stallings',
            'forouzan': 'Data Communications and Networking by Behrouz A. Forouzan',
            'comer': 'Computer Networks and Internets by Douglas Comer',
            'peterson': 'Computer Networks: A Systems Approach by Peterson & Davie',
            'dordal': 'An Introduction to Computer Networks by Peter Dordal',
        }

        for author_key, full_title in author_patterns.items():
            if author_key in clean_name.lower():
                return full_title

        if 'ieee' in clean_name.lower():
            return f"IEEE Standard - {clean_name.title()}"
        elif 'rfc' in clean_name.lower():
            return f"IETF RFC - {clean_name.upper()}"
        elif 'itu' in clean_name.lower():
            return f"ITU-T Recommendation - {clean_name.title()}"

        url_lower = url.lower()
        if 'pearson' in url_lower:
            return f"Pearson Textbook - {clean_name.title()}"
        elif 'mcgraw' in url_lower:
            return f"McGraw-Hill Textbook - {clean_name.title()}"
        elif 'wiley' in url_lower:
            return f"Wiley Textbook - {clean_name.title()}"
        elif 'cengage' in url_lower:
            return f"Cengage Textbook - {clean_name.title()}"

        subject_keywords = {
            'network': 'Computer Networks',
            'protocol': 'Network Protocols',
            'communication': 'Data Communications',
            'internet': 'Internet Technologies',
            'tcp': 'TCP/IP Networking',
            'routing': 'Network Routing',
            'switching': 'Network Switching',
            'security': 'Network Security',
            'wireless': 'Wireless Networks'
        }

        for keyword, subject in subject_keywords.items():
            if keyword in clean_name.lower():
                return f"{subject} - {clean_name.title()}"

        return clean_name.title() if clean_name else "Unknown Textbook"

    def store_url_metadata(self, urls: List[str]) -> Dict[str, Dict[str, str]]:
        url_metadata = {}
        for url in urls:
            metadata = self.extract_textbook_info_from_url(url)
            url_metadata[url] = metadata
            self.url_to_metadata[url] = metadata
        return url_metadata

    def map_files_to_urls(self, txt_files: List[str], downloaded_files: List[str]) -> Dict[str, Dict[str, str]]:
        file_metadata = {}

        downloaded_to_url = self._match_downloaded_files_to_urls(downloaded_files)

        for txt_file in txt_files:
            txt_basename = os.path.basename(txt_file)
            txt_name = os.path.splitext(txt_basename)[0]

            best_match_url = None
            best_match_metadata = None
            best_score = 0

            for downloaded_file, url in downloaded_to_url.items():
                downloaded_basename = os.path.basename(downloaded_file)
                downloaded_name = os.path.splitext(downloaded_basename)[0]

                score = self._calculate_name_similarity(txt_name, downloaded_name)

                if score > best_score and score > 0.3:
                    best_score = score
                    best_match_url = url
                    best_match_metadata = self.url_to_metadata.get(url)

            if best_match_metadata:
                file_metadata[txt_file] = {
                    'title': best_match_metadata['title'],
                    'pdf_url': best_match_url
                }
            else:
                fallback_title = self._extract_title_from_decoded_name(txt_name, "")
                file_metadata[txt_file] = {
                    'title': fallback_title,
                    'pdf_url': f"Local_File_{txt_basename}"
                }

        self.file_to_metadata = file_metadata
        return file_metadata

    def _match_downloaded_files_to_urls(self, downloaded_files: List[str]) -> Dict[str, str]:
        downloaded_to_url = {}

        for downloaded_file in downloaded_files:
            downloaded_basename = os.path.basename(downloaded_file)
            downloaded_name = os.path.splitext(downloaded_basename)[0]

            best_match_url = None
            best_score = 0

            for url, metadata in self.url_to_metadata.items():
                url_filename = metadata.get('filename', '')
                url_name = os.path.splitext(url_filename)[0]

                score = self._calculate_name_similarity(downloaded_name, url_name)

                if score > best_score and score > 0.3:
                    best_score = score
                    best_match_url = url

            if best_match_url:
                downloaded_to_url[downloaded_file] = best_match_url

        return downloaded_to_url

    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        norm1 = self._normalize_filename(name1)
        norm2 = self._normalize_filename(name2)

        if norm1 == norm2:
            return 1.0

        if norm1 in norm2 or norm2 in norm1:
            return 0.8

        words1 = set(re.findall(r'\w+', norm1.lower()))
        words2 = set(re.findall(r'\w+', norm2.lower()))

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _normalize_filename(self, filename: str) -> str:
        normalized = urllib.parse.unquote(filename)
        normalized = re.sub(r'[_\-\s%20]+', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip().lower()
        return normalized

    def save_metadata_to_json(self, filepath: str = "textbook_metadata.json"):
        data = {
            'url_to_metadata': self.url_to_metadata,
            'file_to_metadata': self.file_to_metadata
        }
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Metadata saved to {filepath}")
        except Exception as e:
            print(f"Error saving metadata: {e}")

    def load_metadata_from_json(self, filepath: str = "textbook_metadata.json"):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.url_to_metadata = data.get('url_to_metadata', {})
                self.file_to_metadata = data.get('file_to_metadata', {})
                print(f"Metadata loaded from {filepath}")
        except Exception as e:
            print(f"Error loading metadata: {e}")

    def get_file_metadata(self, file_path: str) -> Optional[Dict[str, str]]:
        return self.file_to_metadata.get(file_path)

    def print_summary(self):
        print(f"\n=== Textbook Metadata Summary ===")
        print(f"URLs processed: {len(self.url_to_metadata)}")
        print(f"Files mapped: {len(self.file_to_metadata)}")

        print("\n--- URL Metadata ---")
        for i, (url, metadata) in enumerate(list(self.url_to_metadata.items())[:3]):
            print(f"{i+1}. URL: {url[:60]}...")
            print(f"   Title: {metadata['title']}")
            print()

        print("\n--- File Metadata ---")
        for i, (file_path, metadata) in enumerate(list(self.file_to_metadata.items())[:3]):
            print(f"{i+1}. File: {os.path.basename(file_path)}")
            print(f"   Title: {metadata['title']}")
            print(f"   URL: {metadata['pdf_url'][:60]}...")
            print()

def extract_textbook_metadata(search_urls: List[str], txt_files: List[str], download_dir: str) -> Dict[str, Dict[str, str]]:
    extractor = TextbookMetadataExtractor()

    # Extract metadata from URLs
    extractor.store_url_metadata(search_urls)

    # List downloaded files from the specified directory
    downloaded_files = []
    if os.path.exists(download_dir):
        for f in os.listdir(download_dir):
            full_path = os.path.join(download_dir, f)
            if not f.startswith('.') and os.path.isfile(full_path):
                downloaded_files.append(full_path)

    # DEBUG: print downloaded files found
    print(f"[DEBUG] Found downloaded files: {downloaded_files}")

    # Map txt files to downloaded files and URLs
    file_metadata = extractor.map_files_to_urls(txt_files, downloaded_files)

    # Print summary
    extractor.print_summary()

    return file_metadata
