from django.conf import settings
from django.db import models

from .utils import email_validator, date_now


# Choices for job titles
# JOBS = (
#     ('0', 'N/A',),
#     ('1', 'Engineer',),
#     ('2', 'Banker',),
#     ('3', 'Computer Engineer',),
#     ('4', 'Teacher',),
#     ('5', 'Lecturer',),
#     ('6', 'Librarian',),
#     ('7', 'Plumber',),
#     ('8', 'Real Estate Agent',),
#     ('9', 'Logistics',),
#     ('10', 'Graphic Designer',),
#     ('11', 'Web Designer',),
#     ('12', 'Woodwork Engineer',),
#     ('13', 'Electrical Engineer',),
#     ('14', 'Ecotourism',),
# )


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'Company: {self.name}'


class EmailModel(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=225,  default='N/A')
    domain = models.URLField(max_length=225,  default='N/A')
    verified = models.BooleanField(default=False)
    position = models.CharField(max_length=225,  default='N/A')
    country = models.CharField(max_length=225, default='N/A')
    company_names = models.ManyToManyField(Company)
    # job_title = models.CharField(choices=JOBS, max_length=2, default='0')
    last_validated = models.DateTimeField(auto_now = True, blank=True)

    def __str__(self):
        return f'ScrapeMail: {self.email}'
    
    def validate(self):
        if self.last_validated:
            now = date_now()
            time_bound = (now - self.last_validated).total_seconds()
            if (time_bound/60/60/24) > settings.VALIDATION_TIME:
                self.verified = email_validator.email_validate(self.email)
                self.last_validated = now
                self.save()
        else:
            return None


class ScrapedLink(models.Model):
    link = models.URLField(default='N/A', max_length=500)
    last_scraped = models.DateTimeField(auto_now = True, blank=True)

    def need_scrape(self):
        if self.last_scraped:
            time_bound = (date_now() - self.last_scraped).total_seconds()
            if (time_bound/60/60/24) > settings.SCRAPING_TIME:
                return True
        else:
            return True

        return False

    def __str__(self):
        return f'ScrapedLink: {self.link}'


class OdinList(models.Model):
    '''
    What we have here is a model/table in the database, we scrape every pages of a websites our users have searched before
    so that we would have scraped every email on those sites to make the users next search faster and more accurate
    '''
    link = models.URLField(default='N/A', max_length=500)
    scraped = models.BooleanField(default=False)
    last_scraped = models.DateTimeField(auto_now = True, blank=True)

    def need_scrape(self):
        if not scraped:
            return True
        if self.last_scraped:
            time_bound = (date_now - self.last_scraped).total_seconds()
            if (time_bound/60/60/24) > settings.SCRAPING_TIME:
                return True
        else:
            return True

        return False

    def __str__(self):
        return f'OdinList: {self.link}'