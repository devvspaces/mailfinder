import datetime
import pytz

from django.db import models


# Choices for job titles
JOBS = (
    ('0', 'N/A',),
    ('1', 'Engineer',),
    ('2', 'Banker',),
    ('3', 'Computer Engineer',),
    ('4', 'Teacher',),
    ('5', 'Lecturer',),
    ('6', 'Librarian',),
    ('7', 'Plumber',),
    ('8', 'Real Estate Agent',),
    ('9', 'Logistics',),
    ('10', 'Graphic Designer',),
    ('11', 'Web Designer',),
    ('12', 'Woodwork Engineer',),
    ('13', 'Electrical Engineer',),
    ('14', 'Ecotourism',),
)


class EmailModel(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=225,  default='N/A')
    domain = models.URLField(max_length=225,  default='N/A')
    verified = models.BooleanField(default=False)
    position = models.CharField(max_length=225,  default='N/A')
    country = models.CharField(max_length=225, default='N/A')
    job_title = models.CharField(choices=JOBS, max_length=2, default='0')
    last_validated = models.DateTimeField(auto_now = True, blank=True)

    def __str__(self):
        return f'ScrapeMail: {self.email}'


class ScrapedLink(models.Model):
    link = models.URLField(default='N/A', max_length=500)
    last_scraped = models.DateTimeField(auto_now = True, blank=True)

    def need_scrape(self):
        if self.last_scraped:
            unaware = datetime.datetime.now()
            now_aware = unaware.replace(tzinfo=pytz.UTC)

            time_bound = (now_aware - self.last_scraped).total_seconds()
            if (time_bound/60/60/24) > 30:
                return True
        else:
            return True

        return False

    def __str__(self):
        return f'ScrapedLink: {self.link}'