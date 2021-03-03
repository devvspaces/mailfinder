from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


from Scraper.models import EmailModel


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None,
                    gender=None, country=None, phone=None,
                    password=None, is_active=True, is_staff=False,
                    is_admin=False):
        if not email:
            raise ValueError("User must provide an email")
        if not first_name:
            raise ValueError("User must provide their First name")
        if not last_name:
            raise ValueError("User must provide their Last name")
        if not country:
            raise ValueError("User must provide their Country")
        if not gender:
            raise ValueError("User must provide their Gender")
        if not phone:
            raise ValueError("User must provide a phone")
        if not password:
            raise ValueError("User must provide a password")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            country=country
        )
        user.set_password(password)
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_staff(self, email, phone=None, first_name=None, last_name=None,
                    gender=None, country=None, password=None):
        user = self.create_user(email=email, first_name=first_name,
                last_name=last_name, gender=gender, country=country,
                phone=phone, password=password, is_staff=True)
        return user

    def create_superuser(self, email, first_name=None, last_name=None,
                    gender=None, country=None, phone=None, password=None):
        user = self.create_user(email=email, first_name=first_name,
                last_name=last_name, gender=gender, country=country,
                phone=phone, password=password, is_staff=True, is_admin=True)
        return user

    def get_staffs(self):
        return self.filter(staff=True)

    def get_admins(self):
        return self.filter(admin=True)


class User(AbstractBaseUser):
    GENDER = (
        ('1', 'Male',),
        ('2', 'Female',),
    )

    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(choices=GENDER, max_length=1)
    country = models.CharField(max_length=3)
    credits = models.IntegerField(default=90)

    # Emails are connected to users, so that they won't pay for emails again
    emails = models.ManyToManyField(EmailModel)

    # Admin fields
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=True)
    
    # Field for disabled accounts
    disabled = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name","last_name","phone",'gender','country']
    USERNAME_FIELD = "email"

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'User {self.email}'
    
    def credit_balance(self):
        credits = self.monthlypayment.get_credit + self.yearlypayment.get_credit + self.oneoffpayment.get_credit + self.specialpayment.get_credit
        return credits
    
    def deduct_credit(self, amount):
        precedence = [self.oneoffpayment, self.monthlypayment, self.yearlypayment, self.specialpayment]
        for i in precedence:
            if i.get_credit >= amount:
                i.credits -= amount
                i.save()
                break
    
    @property
    def user_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('profile', kwargs = [self.id])

    def email_user(self, subject, message, fail=True):
        print(message)
        val = send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[self.email], fail_silently=fail)
        return True if val else False

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = 'MailFinder User'