from django.db import models


class EmailModel(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=225,  default='N/A')
    domain = models.URLField(max_length=225,  default='N/A')
    verified = models.BooleanField(default=False)
    position = models.CharField(max_length=225,  default='N/A')
    country = models.CharField(max_length=225, default='N/A')
    last_validated = models.DateTimeField(auto_now_add = True, blank=True)

    def __str__(self):
        return f'ScrapeMail: {self.email}'