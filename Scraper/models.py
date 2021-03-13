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
    phone_number = models.CharField(max_length=225,  default='N/A')

    position = models.CharField(max_length=225,  default='N/A')
    department = models.CharField(max_length=225,  default='N/A')
    seniority = models.CharField(max_length=1, default='1', choices=settings.SENIOR_TYPE)

    company_names = models.ManyToManyField(Company)
    email_type = models.CharField(max_length=1, default='1', choices=settings.EMAIL_TYPE)

    linkedin = models.CharField(max_length=225,  default='N/A')
    twitter = models.CharField(max_length=225,  default='N/A')

    # job_title = models.CharField(choices=JOBS, max_length=2, default='0')
    last_validated = models.DateTimeField(auto_now = True, blank=True)

    def __str__(self):
        return f'ScrapeMail: {self.email}'
    
    @property
    def country(self):
        res = OdinList.objects.filter(domain__exact=self.domain).first()
        if res:
            return res.country
        return 'N/A'
    
    def needs_validation(self):
        if self.last_validated:
            now = date_now()
            time_bound = (now - self.last_validated).total_seconds()
            if (time_bound/60/60/24) > settings.VALIDATION_TIME:
                return True
            else:
                return False
        else:
            return None
    
    def validate(self):
        needs = self.needs_validation()
        if needs:
            now = date_now()
            self.verified = email_validator.email_validate(self.email)
            self.last_validated = now
            self.save()
        elif needs == False:
            return False





class OdinList(models.Model):
    '''
    What we have here is a model/table in the database, we scrape every pages of a websites our users have searched before
    so that we would have scraped every email on those sites to make the users next search faster and more accurate
    '''
    domain = models.URLField(default='N/A', max_length=500, unique=True)
    scraped = models.BooleanField(default=False)
    last_scraped = models.DateTimeField(auto_now = True, blank=True)
    disposable = models.BooleanField(default=False)
    webmail = models.BooleanField(default=False)
    organization = models.CharField(default='N/A', max_length=255)
    country = models.CharField(default='N/A', max_length=255)
    state = models.CharField(default='N/A', max_length=255)

    def need_scrape(self):
        if not self.scraped:
            return True
        if self.last_scraped:
            time_bound = (date_now - self.last_scraped).total_seconds()
            if (time_bound/60/60/24) > settings.SCRAPING_TIME:
                return True
        else:
            return True

        return False
    
    def reset_children(self):
        for i in self.scrapedlink_set.all():
            i.beta_searched = False
            i.save()
    
    def new_links(self):
        links = set()
        for i in self.scrapedlink_set.all():
            # Check if this url is not permitted
            if i.link.find('#') != 1:
                i.delete()
            elif i.beta_searched == False:
                links.add(i.link)
        return list(links)

    def __str__(self):
        return f'OdinList: {self.link}'




class ScrapedLink(models.Model):
    parent_link = models.ForeignKey(OdinList, on_delete=models.DO_NOTHING, null=True)
    link = models.URLField(default='N/A', max_length=500, unique=True)
    last_scraped = models.DateTimeField(auto_now = True, blank=True)
    beta_searched = models.BooleanField(default=False)

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