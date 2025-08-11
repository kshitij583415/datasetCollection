# import csv
# import os
# from config import PROCESSED_INDEX

# def load_processed_index():
#     """Loads the set of processed file paths from the CSV index file."""
#     if os.path.exists(PROCESSED_INDEX):
#         try:
#             with open(PROCESSED_INDEX, "r", encoding="utf-8", newline="") as f:
#                 reader = csv.reader(f)
#                 # The file contains one path per row.
#                 # Each row will be a list with one element.
#                 return {row[0] for row in reader if row}
#         except (IOError, csv.Error):
#             return set()  # Return empty set if file is corrupt or not a list
#     return set()

# def save_processed_index(processed_set):
#     """Saves the set of processed file paths to the CSV index file."""
#     with open(PROCESSED_INDEX, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         # Write each path as a new row in the CSV, sorted for consistency
#         for path in sorted(list(processed_set)):
#             writer.writerow([path])


import csv
import os
from config import PROCESSED_INDEX

def load_processed_index():
    """Loads the processed file information from the CSV index file.
    
    Returns:
        dict: Dictionary with file_path as key and dict with title, pdf_url, file_size as value
        set: For backward compatibility, also returns a set of processed file paths
    """
    processed_dict = {}
    processed_set = set()
    
    if os.path.exists(PROCESSED_INDEX):
        try:
            with open(PROCESSED_INDEX, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                
                # Check if file has headers
                if reader.fieldnames is None:
                    return processed_dict, set()
                
                for row in reader:
                    # Handle both old format (just paths) and new format (with details)
                    if 'Title' in row and 'pdf_url' in row and 'File_Size_KB' in row:
                        # New format with full details
                        file_path = row.get('File_Path', '')
                        if file_path:
                            processed_dict[file_path] = {
                                'title': row['Title'],
                                'pdf_url': row['pdf_url'],
                                'file_size_kb': row['File_Size_KB']
                            }
                            processed_set.add(file_path)
                    else:
                        # Handle old format or missing columns
                        for key, value in row.items():
                            if value and os.path.exists(value):  # Assume it's a file path
                                processed_set.add(value)
                                processed_dict[value] = {
                                    'title': 'Unknown',
                                    'pdf_url': 'Unknown',
                                    'file_size_kb': 'Unknown'
                                }
                                
        except (IOError, csv.Error) as e:
            print(f"Error reading processed index: {e}")
            return {}, set()
    
    return processed_dict, processed_set

def save_processed_index(processed_data):
    """Saves the processed file information to the CSV index file.
    
    Args:
        processed_data: Can be either:
            - set: For backward compatibility (file paths only)
            - dict: New format with file_path as key and details as value
    """
    try:
        with open(PROCESSED_INDEX, "w", encoding="utf-8", newline="") as f:
            fieldnames = ['Title', 'pdf_url', 'File_Size_KB', 'File_Path']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            if isinstance(processed_data, set):
                # Backward compatibility: convert set to dict format
                for file_path in sorted(processed_data):
                    writer.writerow({
                        'Title': 'Unknown',
                        'pdf_url': 'Unknown',
                        'File_Size_KB': get_file_size_kb(file_path),
                        'File_Path': file_path
                    })
            elif isinstance(processed_data, dict):
                # New format: full details
                for file_path, details in sorted(processed_data.items()):
                    writer.writerow({
                        'Title': details.get('title', 'Unknown'),
                        'pdf_url': details.get('pdf_url', 'Unknown'),
                        'File_Size_KB': details.get('file_size_kb', get_file_size_kb(file_path)),
                        'File_Path': file_path
                    })
    except (IOError, csv.Error) as e:
        print(f"Error saving processed index: {e}")

def get_file_size_kb(file_path):
    """Get file size in KB.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File size in KB or 'Unknown' if file doesn't exist
    """
    try:
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            size_kb = round(size_bytes / 1024, 2)
            return str(size_kb)
        else:
            return 'Unknown'
    except OSError:
        return 'Unknown'

def add_processed_file(file_path, title=None, pdf_url=None, file_size_kb=None):
    """Add a single processed file to the index.
    
    Args:
        file_path (str): Path to the processed file
        title (str, optional): Title of the document
        pdf_url (str, optional): Original PDF URL
        file_size_kb (str, optional): File size in KB
    """
    processed_dict, _ = load_processed_index()
    
    # Auto-calculate file size if not provided
    if file_size_kb is None:
        file_size_kb = get_file_size_kb(file_path)
    
    processed_dict[file_path] = {
        'title': title or 'Unknown',
        'pdf_url': pdf_url or 'Unknown',
        'file_size_kb': file_size_kb
    }
    
    save_processed_index(processed_dict)

def is_file_processed(file_path):
    """Check if a file has already been processed.
    
    Args:
        file_path (str): Path to check
        
    Returns:
        bool: True if file is already processed
    """
    _, processed_set = load_processed_index()
    return file_path in processed_set

def get_processed_file_info(file_path):
    """Get detailed information about a processed file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: File information or None if not found
    """
    processed_dict, _ = load_processed_index()
    return processed_dict.get(file_path)

def print_processed_index_summary():
    """Print a summary of the processed index."""
    processed_dict, processed_set = load_processed_index()
    
    print(f"\n=== Processed Index Summary ===")
    print(f"Total processed files: {len(processed_set)}")
    
    if processed_dict:
        print("\nRecent entries:")
        for i, (file_path, details) in enumerate(sorted(processed_dict.items())[-5:]):
            print(f"{i+1}. Title: {details['title'][:50]}...")
            print(f"   URL: {details['pdf_url']}")
            print(f"   Size: {details['file_size_kb']} KB")
            print(f"   Path: {file_path}")
            print()

# Backward compatibility functions
def load_processed_set():
    """Backward compatibility function - returns only the set of processed paths."""
    _, processed_set = load_processed_index()
    return processed_set

def save_processed_set(processed_set):
    """Backward compatibility function - saves only the set of processed paths."""
    save_processed_index(processed_set)