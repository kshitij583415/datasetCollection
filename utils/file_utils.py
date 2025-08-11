import os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def file_exists(path):
    return os.path.exists(path)

def is_textbook(content):
    """Basic check if file content looks like a textbook."""
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in ["chapter", "contents", "lesson", "unit"])

def list_files(folder, extensions=None):
    files = []
    for f in os.listdir(folder):
        if extensions:
            if any(f.lower().endswith(ext) for ext in extensions):
                files.append(os.path.join(folder, f))
        else:
            files.append(os.path.join(folder, f))
    return files
