from bs4 import BeautifulSoup as bs
import requests
import re

EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

# req = requests.get('http://www.email-database.info/').text.replace('-','@')

# with open('more.html','w') as f:
#     f.write(req)
with open('more.html','r') as f:
    soup = bs(f.read(), 'lxml')

match = soup.find_all('a', class_='titleNews')
links = [i['href'].replace('@','-') for i in match]

emails = []

# Scrape emails
for i in links:
    req = requests.get(i).text.replace('-','@')
    rate = re.finditer(EMAIL_REGEX, req)
    for i in rate:
        emails.append(i.group(0))
    print('Done', i)

with open('email.csv','a') as f:
    for i in emails:
        f.write(i)
        f.write('\n')
    print('Completed CSV')