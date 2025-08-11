from googleapiclient.discovery import build
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID, NUM_RESULTS

def search_itut_papers(query):
    """
    Search for ITU-T papers related to the given query.
    Filters for PDF documents from the official ITU-T domain.
    """
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    
    # Restrict search to ITU-T's domain and add query keyword
    search_query = f"site:itu.int {query} filetype:pdf"
    
    res = service.cse().list(q=search_query, cx=GOOGLE_CSE_ID, num=NUM_RESULTS).execute()
    urls = []
    
    for item in res.get("items", []):
        link = item.get("link")
        if link and link.lower().endswith(".pdf"):
            urls.append(link)
    
    return urls
