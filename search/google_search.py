from googleapiclient.discovery import build
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID, NUM_RESULTS

def search_textbooks(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=NUM_RESULTS).execute()
    urls = []
    for item in res.get("items", []):
        link = item.get("link")
        if link and any(link.lower().endswith(ext) for ext in [".pdf", ".docx", ".txt", ".epub"]):
            urls.append(link)
    return urls
