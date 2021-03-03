from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError
import httplib2
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlunparse
from urllib.request import urlopen, Request

from django.conf import settings

from .models import ScrapedLink



try:
    # Create the discovery build once here, when project runs
    service = build("customsearch", "v1", developerKey=settings.GOOGLE_SEARCH_API_KEY)
    res = service.cse()
except httplib2.error.ServerNotFoundError:
    pass


def searchBing(query, num_links=20, unique=True):
    result_links = set()
    # Parsing the query and making the request
    url = urlunparse(("https", "www.bing.com", "/search", "", urlencode({"q": query}), ""))
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    req = Request(url, headers={"User-Agent": custom_user_agent})
    page = urlopen(req)

    # Setting list of links to avoid
    avoid = ['chrome.google.com','www.microsofttranslator.com','play.google.com']

    # Converting the response to a soup and getting result links from it and next pages
    soup = BeautifulSoup(page.read(), 'lxml')
    
    # Getting result links
    b_results = soup.find('ol', id='b_results')
    links = b_results.findAll("a")
    for link in links:
        try:
            get_link = link["href"]
            if (get_link.startswith('http') or get_link.startswith('www')) and (not get_link.startswith('/')):
                for i in avoid:
                    if get_link.find(i) != -1:
                        break
                else:
                    result_links.add(link["href"])
        except KeyError:
            pass
    
    next_page_number=1
    
    
    while len(result_links) < num_links:
        # Getting next pages
        try:
            q=[urlencode({"q": query}),urlencode({"first": str(next_page_number)+'1'}),urlencode({"FORM": 'PERE'+(str(next_page_number-1) if (next_page_number-1) > 0 else '')})]
            next_page_link = '&'.join(q)
            # print(q)
        except:
            break
        
        # Scrape the contents of the new url
        try:
            url = urlunparse(("https", "www.bing.com", "/search", "", next_page_link, ""))
            custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
            req = Request(url, headers={"User-Agent": custom_user_agent})
            page = urlopen(req)
            soup = BeautifulSoup(page.read(), "lxml")

            # Getting result links
            b_results = soup.find('ol', id='b_results')
            links = b_results.findAll("a")
            for link in links:
                try:
                    get_link = link["href"]
                    if (get_link.startswith('http') or get_link.startswith('www')) and (not get_link.startswith('/')):
                        # If unique is true this means that the links returned must not have been scraped before
                        if unique:
                            obj = ScrapedLink.objects.filter(link__exact=get_link).first()
                            if obj:
                                if obj.need_scrape():
                                    result_links.add(get_link)
                            else:
                                for i in avoid:
                                    if get_link.find(i) != -1:
                                        break
                                else:
                                    result_links.add(get_link)
                        else:
                            for i in avoid:
                                if get_link.find(i) != -1:
                                    break
                            else:
                                result_links.add(get_link)
                except KeyError:
                    pass
            next_page_number+=1
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            break

    return list(result_links)



def google_search(search_term, **kwargs):
    try:
        res = res.list(q=search_term, cx=settings.GOOGLE_CSE_ID, **kwargs)
    except UnboundLocalError:
        service = build("customsearch", "v1", developerKey=settings.GOOGLE_SEARCH_API_KEY)
        res = service.cse()
        res = res.list(q=search_term, cx=settings.GOOGLE_CSE_ID, **kwargs)
    try:
        res = res.execute()
    except:
        return None
    return res

def searchGoogle(search, num_links=20):
    links = set()
    nums = [(i*10)+1 for i in range(num_links)]
    
    for i in nums:
        result = google_search(search, num=10, start=i)
        # print(result)
        if result is not None:
            try:
                for i in result['items']:
                    links.add(i['link'])
                
                # Loop through the results, Check if the links have been recently scraped
                for i in list(links):
                    try:
                        obj = ScrapedLink.objects.get(link__exact=i)
                        if obj.need_scrape() == False:
                            links.discard(i)
                    except ScrapedLink.DoesNotExist:
                        pass
                
                # Break loop if links is up to required links
                if len(links) > num_links:
                    break
            except:
                break
            print(list(links))
            return list(links)
        else:
            return searchBing(search, num_links)


