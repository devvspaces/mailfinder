import json
from pyhunter import PyHunter

from django.conf import settings

from .models import EmailModel, OdinList, Company



# This is the hunter.io api code
class HunterIO:
    def __init__(self, api_key):
        # Initializing the pyhunter object with our api key
        self.hunter = PyHunter(api_key)
        self.accepted = ['valid']
    
    def get_value(self, tup, value):
        for i in tup:
            if i[1] == value:
                return i[0]
        return '0'
    
    def clean_value(self, value):
        if value is None:
            return 'N/A'
        return value

    def build_odin_obj(self, domain, organization='', disposable='', webmail='', country='', state=''):
        # Creating the domain odin's obj
        url_search = OdinList.objects.filter(domain__exact=domain)
        if url_search.exists() == False:
            obj = OdinList.objects.create(
                domain = self.clean_value(domain),
                organization = self.clean_value(organization),
                disposable = self.clean_value(disposable),
                webmail = self.clean_value(webmail),
                country = self.clean_value(country),
                state = self.clean_value(state),
            )
        else:
            obj = url_search.first()
        return obj
    
    def create_company(self, name):
        if name is not None:
            # Check if the company already exists in our db
            company_search = Company.objects.filter(name__exact=name)

            if company_search.exists():
                company = company_search.first()
            else:
                # Creating the company name
                value_c = self.clean_value(name)
                company = Company.objects.create(name=value_c)
            return company


    def domain_search(self, domain_name='', company_name=''):
        result = self.hunter.domain_search(domain_name, company_name)
        
        # Initializing results set for the emails found
        results_set = set()
        
        # Getting all required results
        disposable = result['disposable']
        webmail = result['webmail']
        organization = result['organization']
        country = result['country']
        state = result['state']
        domain_name = result['domain']

        # Build the odins obj
        if domain_name:
            self.build_odin_obj(domain_name, organization, disposable, webmail, country, state)
        
        # Creating the company
        company = self.create_company(organization)
        
        # Looping through the email results returned and creating emails
        for email in result['emails']:
            value = email['value']
            
            email_type = self.get_value(settings.EMAIL_TYPE, email['type'])
            # confidence = email['confidence']
            name = f"{email['first_name']} {email['last_name']}"
            position = email['position']
            seniority = self.get_value(settings.SENIOR_TYPE, email['seniority'])
            department = email['department']
            linkedin = email['linkedin']
            twitter = email['twitter']
            phone_number = email['phone_number']
            status = email['verification']['status']

            # Check if the email already exists
            email_res = EmailModel.objects.filter(email__exact=value)
            if email_res.exists():
                email_obj = email_res.first()
            else:
                # Creating the new email objects
                email_obj = EmailModel.objects.create(
                    email = self.clean_value(value),
                    name = self.clean_value(name),
                    domain = self.clean_value(domain_name),
                    position = self.clean_value(position),
                    seniority = self.clean_value(seniority),
                    department = self.clean_value(department),
                    email_type = self.clean_value(email_type),
                    linkedin = self.clean_value(linkedin),
                    twitter = self.clean_value(twitter),
                    phone_number = self.clean_value(phone_number),
                )

            # Adding the organization name to the email object
            if company:
                email_obj.company_names.add(company)

            # Is the email object verified or not
            if status in self.accepted:
                email_obj.verified = True
            else:
                email_obj.verified = False
            email_obj.save()

            # Adding the email object to the result set
            results_set.add(email_obj)
        
        return list(results_set)
    
    def find_email(self, name, company):
        result = self.hunter.email_finder(company=company, full_name=name)

        # Getting all required results
        name = f"{result['first_name']} {result['last_name']}"
        email = result['email']
        domain = result['domain']
        position = result['position']
        twitter = result['twitter']
        linkedin_url = result['linkedin_url']
        phone_number = result['phone_number']
        company = result['company']
        status = result['status']

        # Build the odins obj
        if domain:
            self.build_odin_obj(domain, company)
        
        # Creating the company
        company = self.create_company(company)

        # Getting the linkedin username from the url
        linkedin = linkedin_url.split('/')[-1]


        # Check if the email already exists
        email_res = EmailModel.objects.filter(email__exact=email)
        if email_res.exists():
            email_obj = email_res.first()
        else:
            # Creating the new email objects
            email_obj = EmailModel.objects.create(
                email = self.clean_value(email),
                name = self.clean_value(name),
                domain = self.clean_value(domain),
                position = self.clean_value(position),
                linkedin = self.clean_value(linkedin),
                twitter = self.clean_value(twitter),
                phone_number = self.clean_value(phone_number),
            )

            # Adding the organization name to the email object
            if company:
                email_obj.company_names.add(company)

        # Is the email object verified or not
        if status in self.accepted:
            email_obj.verified = True
        else:
            email_obj.verified = False
        email_obj.save()

        return email_obj
    
    def verify_email(self, email):
        result = self.hunter.email_verifier(email)

        # Getting all required results
        email = result['email']
        domain = email.split('@')[-1]
        disposable = result['disposable']
        webmail = result['webmail']
        status = result['status']

        # Build the odins obj
        if domain:
            self.build_odin_obj(domain, disposable=disposable, webmail=webmail)

        # Check if the email already exists
        email_res = EmailModel.objects.filter(email__exact=email)
        if email_res.exists():
            email_obj = email_res.first()
        else:
            # Creating the new email objects
            email_obj = EmailModel.objects.create(
                email = self.clean_value(email),
                domain = self.clean_value(domain)
            )

        # Is the email object verified or not
        if status in self.accepted:
            email_obj.verified = True
        else:
            email_obj.verified = False
        email_obj.save()

        return email_obj
    
    def verify_emails(self, emails=None):
        if emails is None:
            emails = []
        
        # Initializing emails set
        email_set = set()
        
        for email in emails:
            email_set.add(self.verify_email(email))
        
        return list(email_set)


email_hunter = HunterIO(api_key=settings.HUNTER_API_KEY)