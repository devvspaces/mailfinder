from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError
import httplib2

from django.conf import settings

from .models import ScrapedLink
from .utils import searchBing



try:
    # Create the discovery build once here, when project runs
    service = build("customsearch", "v1", developerKey=settings.GOOGLE_SEARCH_API_KEY)
    res = service.cse()
except httplib2.error.ServerNotFoundError:
    pass


def google_search(search_term, **kwargs):
    try:
        res = res.list(q=search_term, cx=settings.GOOGLE_CSE_ID, **kwargs)
    except UnboundLocalError:
        service = build("customsearch", "v1", developerKey=settings.GOOGLE_SEARCH_API_KEY)
        res = service.cse()
        res = res.list(q=search_term, cx=settings.GOOGLE_CSE_ID, **kwargs)
    try:
        res = res.execute()
    except GoogleHttpError:
        return None
    return res

def searchGoogle(search, num_links=20):
    links = set()
    nums = [(i*10)+1 for i in range(num_links)]
    
    for i in nums:
        result = google_search(search, num=10, start=i)
        if result_links is not None:
            try:
                for i in result['items']:
                    links.add(i['link'])
                
                # Loop through the results, Check if the links have been recently scraped
                for i in list(links):
                    try:
                        obj = ScrapedLink.objects.get(link=i)
                        if obj.need_scrape() == False:
                            links.discard(i)
                    except ScrapedLink.DoesNotExist:
                        pass
                
                # Break loop if links is up to required links
                if len(links) > num_links:
                    break
            except:
                break
            return list(links)
        else:
            return searchBing(search, num_links)