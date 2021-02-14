from googleapiclient.discovery import build

from django.conf import settings


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def search_google(search)
    links = set()
    result = google_search(search, settings.GOOGLE_SEARCH_API_KEY, settings.GOOGLE_CSE_ID)
    for i in result['items']:
        links.add(i['link'])
    return list(links)