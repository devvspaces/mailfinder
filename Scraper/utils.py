import time
import re
import dns.resolver
from disposable_email_checker.emails import email_domain_loader
import pydnsbl
import socket
import smtplib

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from disposable_email_checker.validators import validate_disposable_email

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
            mx_records = self.resolve_mx_record(email):
            if mx_records != False:
                if self.is_disposable_email(email) == False:
                    if self.email_ip_blacklist(email) == False:
                        if self.check_email(emial):
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
        time.sleep(2)
        host = socket.gethostname()

        for mx in mxRecords:
            try:
                server = smtplib.SMTP()
                server.set_debuglevel(0)
                addressToVerify = email
                server.connect(mx)
                server.helo(host)
                server.mail('me@domain.com')
                code, message = server.rcpt(str(addressToVerify))
                server.quit()
                if code == 250:
                    return True
            except:
                pass
        
        return False

# Instance of validator
email_validator = EmailPackageValidator()