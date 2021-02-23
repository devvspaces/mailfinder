from googleapiclient.discovery import build
import httplib2

from django.conf import settings

from .models import ScrapedLink



try:
    # Create the discovery build once here, when project runs
    service = build("customsearch", "v1", developerKey=settings.GOOGLE_SEARCH_API_KEY)
    res = service.cse()
except httplib2.error.ServerNotFoundError:
    pass


def google_search(search_term, **kwargs):
    # service = build("customsearch", "v1", developerKey=api_key)
    # res = service.cse()
    try:
        res = res.list(q=search_term, cx=settings.GOOGLE_CSE_ID, **kwargs)
    except UnboundLocalError:
        service = build("customsearch", "v1", developerKey=settings.GOOGLE_SEARCH_API_KEY)
        res = service.cse()
        res = res.list(q=search_term, cx=settings.GOOGLE_CSE_ID, **kwargs)
    # print('the list object', dir(res), help(res), res)
    res = res.execute()
    return res

def searchGoogle(search, num_links=20):
    links = set()
    nums = [(i*10)+1 for i in range(num_links)]
    for i in nums:
        result = google_search(search, num=10, start=i)
        # print(result['queries']['request'][0]['totalResults'])
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