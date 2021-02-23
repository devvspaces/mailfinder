from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import re
import time


from .models import ScrapedLink



def get_emails_from_page(url):
    url = 'http://'+url if not url.startswith('http') else url

    # a queue of urls to be crawled next
    new_urls = deque([url])

    # a set of urls that we have already processed
    processed_urls = set()

    # a set of domains inside the target website
    local_urls = set()

    # a set of domains outside the target website
    foreign_urls = set()

    # a set of broken urls
    broken_urls = set()

    emails = set()

    man=0

    # process urls one by one until we exhaust the queue
    start = time.time()
    while len(new_urls):
        man+=1
        # move url from the queue to processed url set
        url = new_urls.popleft()
        processed_urls.add(url)
        if (url.find('#') == -1) or (url.find('@') != -1):
            # print the current url
            # print("Processing %s" % url)
            try:
                response = requests.get(url)

                # extract base url to resolve relative links
                parts = urlsplit(url)
                base = "{0.netloc}".format(parts)
                strip_base = base.replace("www.", "")
                base_url = "{0.scheme}://{0.netloc}".format(parts)
                path = url[:url.rfind('/')+1] if '/' in parts.path else url

                soup = BeautifulSoup(response.text, "lxml")

                new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
                emails.update(new_emails)
                print('\n\n',emails, url)


                # Check if the url have been added if not then add it
                try:
                    obj = ScrapedLink.objects.get(link=url)
                    # Updated the last scraped date
                    obj.save()
                except ScrapedLink.DoesNotExist:
                    obj = ScrapedLink.objects.create(link=url)

                if (time.time()-start)>(10):
                    break

                for link in soup.find_all('a'):
                    # extract link url from the anchor
                    anchor = link.attrs['href'] if 'href' in link.attrs else ''

                    if anchor.startswith('/'):
                        local_link = base_url + anchor
                        local_urls.add(local_link)
                    elif strip_base in anchor:
                        local_urls.add(anchor)
                    elif not anchor.startswith('http'):
                        local_link = path + anchor
                        local_urls.add(local_link)
                    else:
                        foreign_urls.add(anchor)
                    
                for i in local_urls:
                    if not i in new_urls and not i in processed_urls:
                        # Check if the url have been added if not then add it
                        try:
                            obj = ScrapedLink.objects.get(link=i)
                            if obj.need_scrape() == True:
                                new_urls.append(i)
                        except ScrapedLink.DoesNotExist:
                            obj = ScrapedLink.objects.create(link=i)
                            new_urls.append(i)
                    
                if not link in new_urls and not link in processed_urls:
                    # Check if the url have been added if not then add it
                    try:
                        obj = ScrapedLink.objects.get(link=link)
                        if obj.need_scrape() == True:
                            new_urls.append(link)
                    except ScrapedLink.DoesNotExist:
                        obj = ScrapedLink.objects.create(link=link)
                        new_urls.append(link)
            except(TypeError, requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                # add broken urls to it’s own set, then continue
                broken_urls.add(url)
                continue
    
    return list(emails)

# print(emails)
# print('Local urls\n',local_urls)
# print('Processed urls\n',processed_urls)
# print('Foreign urls\n',foreign_urls)
# print('Broken urls\n',broken_urls)


def get_emails_from_links(links=None):
    emails = set()
    if links is None:
        links = []
    
    for link in links:
        try:
            response = requests.get(link)
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
            emails.update(new_emails)

            # Check if the link have been added if not then add it
            try:
                obj = ScrapedLink.objects.get(link=link)
                # Updated the last scraped date
                obj.save()
            except ScrapedLink.DoesNotExist:
                obj = ScrapedLink.objects.create(link=link)
        except(TypeError, requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            continue
    
    return list(emails)