import re

with open('test.csv','r') as f:
    response = f.read()
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response, re.I))
    print(new_emails)