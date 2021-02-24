import time
import re
import dns.resolver
from disposable_email_checker.emails import email_domain_loader
import pydnsbl
import socket
import smtplib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlunparse
from urllib.request import urlopen, Request

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from disposable_email_checker.validators import validate_disposable_email

from .models import EmailModel, ScrapedLink



def email_format(emails=None):
    if emails is None:
        emails = []
    emails = list(set([i.lower() for i in emails]))
    processed=set()
    for i in emails:
        try:
            validate_email(i)
            processed.add(i)
        except ValidationError:
            pass
    
    return list(processed)
        


def clean_emails(emails=None, domain=''):
    if emails is None:
        emails = []
    emails = list(set([i.lower() for i in emails]))
    processed=set()
    for i in emails:
        splited_email = i.split('@')

        # Check for required domains
        if domain:
            if splited_email[-1] == domain.lower():
                processed.add(i)
        
    return list(processed)
        

def get_extra_deas():
    # This gets all the emails from dea list i have
    try:
        with open('disposable-email-domains/disposable_email_blocklist.conf') as fig:
            return [i.replace('\n','') for i in fig.readlines()]
    except:
        return []

# Creating email validation class
class EmailPackageValidator:
    def __init__(self, *args, **kwargs):
        # Get get_extra_deas() and add to a variable
        self.DEAS = get_extra_deas()
        pass
    
    def email_validate(self, email):
        # This functions calls other functions to validate this email and returns true and status of validation
        
        # First check the email syntax
        if self.is_email_valid(email):
            # Get the mx records
            mx_records = self.resolve_mx_record(email)
            if mx_records != False:
                if self.is_disposable_email(email) == False:
                    # Get the domain of the email
                    domain = email.split('@')[-1]
                    if self.email_ip_blacklist(domain) == False:
                        if self.check_email(email, mx_records):
                            # The email is valid if it passes all this validation
                            return True
        
        return False

    
    def is_email_valid(self, email):
        try:
            validate_email(email)
        except ValidationError:
            return False
        return True

    def resolve_mx_record(self, email):
        # Get email domain from email
        domain = email.split('@')[-1]

        # MX record lists
        mx_records = []

        try:
            for x in dns.resolver.resolve(domain, 'MX'):
                mx_records.append(tuple(x.to_text().split(' ')))

            # print(mx_records)
            return sorted(mx_records)
        except:
            pass
        
        return False

    def is_disposable(self, email):
        try:
            validate_disposable_email(email)
        except ValidationError:
            return True
        return False

    def is_disposable_email(self, email):
        try:
            email_domain = email.split('@')[-1]

            # First check is_disposable(email)
            val = self.is_disposable(email)
            if val:
                return val

            # Use list here
            if email_domain not in self.DEAS:
                return False
        except:
            pass

        return True

    def email_ip_blacklist(self, domain):
        domain_checker = pydnsbl.DNSBLDomainChecker()
        dnsbl = domain_checker.check(domain)
        if dnsbl.blacklisted:
            return True
        return False


    def check_email(self, email, mxRecords):
        # time.sleep(2)
        host = socket.gethostname()
        PORTS=[25, 587, 465, 2525]

        server = smtplib.SMTP()
        for mx in mxRecords:
            server.set_debuglevel(0)
            addressToVerify = email
            for i in PORTS:
                print('I ran this ports')
                try:
                    server.connect(mx[1], port=i)
                    server.helo(host)
                    server.mail('me@domain.com')
                    code, message = server.rcpt(str(addressToVerify))
                    print(code, message)
                    server.quit()
                    if code == 250:
                        return True
                    elif code == 550:
                        break
                except (TimeoutError, OSError):
                    pass
        return False

# Instance of validator
email_validator = EmailPackageValidator()




def searchBing(query, num_links=20):
    result_links = set()
    # Parsing the query and making the request
    url = urlunparse(("https", "www.bing.com", "/search", "", urlencode({"q": query}), ""))
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    req = Request(url, headers={"User-Agent": custom_user_agent})
    page = urlopen(req)

    # Converting the response to a soup and getting result links from it and next pages
    soup = BeautifulSoup(page.read(), 'lxml')
    
    # Getting result links
    b_results = soup.find('ol', id='b_results')
    links = b_results.findAll("a")
    for link in links:
        try:
            get_link = link["href"]
            if (get_link.startswith('http') or get_link.startswith('www')) and (not get_link.startswith('/')):
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
                        obj = ScrapedLink.objects.filter(link__exact=get_link).first()
                        if obj:
                            if obj.need_scrape():
                                result_links.add(get_link)
                        else:
                            result_links.add(get_link)
                except KeyError:
                    pass
            next_page_number+=1
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            break

    return list(result_links)