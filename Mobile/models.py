from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'Subscriber: {self.email}'
