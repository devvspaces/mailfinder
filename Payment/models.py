from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from Account.models import User
from Scraper.utils import date_now


class Amount(models.Model):
    CHOICES = (
        ('1', 'Monthly Payment',),
        ('2', 'Yearly Payment',),
        ('3', 'One-off Payment',),
        ('4', 'Special Payment',),
    )
    amount = models.FloatField()
    price = models.FloatField()
    price = models.CharField(choices=CHOICES, max_length=1, default='3')

    def __str__(self):
        return f'Amount: {self.amount} emails for ${self.price}'


class MonthlyPayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=True)

    @property
    def get_credit(self):
        now = date_now()
        total_seconds = (now - self.updated).total_seconds()
        if total_seconds/60/60/24 > 30:
            # Call reocurring payment function
            return 0
        else:
            return int(self.credits)
        
        return 0

    def __str__(self):
        return f'Monthly Payment: {self.user.first_name} {self.credits}'


class YearlyPayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=True)

    @property
    def get_credit(self):
        now = date_now()
        total_seconds = (now - self.updated).total_seconds()
        if total_seconds/60/60/24/365 > 10:
            # Call reocurring payment function
            return 0
        else:
            return int(self.credits)
        
        return 0

    def __str__(self):
        return f'Yearly Payment: {self.user.first_name} {self.credits}'


class OneoffPayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    started = models.DateTimeField(auto_now_add=True)

    @property
    def get_credit(self):
        now = date_now()
        total_seconds = (now - self.started).total_seconds()
        if total_seconds/60/60/24 > 30:
            self.credits = 0
            self.save()
        return int(self.credits)

    def __str__(self):
        return f'Oneoff Payment: {self.user.first_name} {self.credits}'


class SpecialPayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    started = models.DateTimeField(auto_now_add=True)

    @property
    def get_credit(self):
        # now = date_now()
        # total_seconds = (now - self.updated).total_seconds()
        # if total_seconds/60/60/24 > 30:
        #     self.credits = 0
        #     self.save()
        return int(self.credits)

    def __str__(self):
        return f'Special Payment: {self.user.first_name} {self.credits}'



# Our signals
@receiver(post_save, sender=User)
def create_payments_objects(sender, instance, created, **kwargs):
    if created:
        OneoffPayment.objects.create(user=instance, credits=90)
    # Check if the user has any of this objects if none then create one for them
    if not MonthlyPayment.objects.filter(user=instance).exists():
        MonthlyPayment.objects.create(user=instance)
    if not YearlyPayment.objects.filter(user=instance).exists():
        YearlyPayment.objects.create(user=instance)
    if not OneoffPayment.objects.filter(user=instance).exists():
        OneoffPayment.objects.create(user=instance)
    if not SpecialPayment.objects.filter(user=instance).exists():
        SpecialPayment.objects.create(user=instance)