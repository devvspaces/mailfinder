from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import re

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

    # process urls one by one until we exhaust the queue
    while len(new_urls):
        # move url from the queue to processed url set
        url = new_urls.popleft()
        processed_urls.add(url)
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
            # print(emails)

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
                    new_urls.append(i)
                
            if not link in new_urls and not link in processed_urls:
                new_urls.append(link)
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            # add broken urls to it’s own set, then continue
            broken_urls.add(url)
            continue
    
    return list(emails)

# print(emails)
# print('Local urls\n',local_urls)
# print('Processed urls\n',processed_urls)
# print('Foreign urls\n',foreign_urls)
# print('Broken urls\n',broken_urls)
    