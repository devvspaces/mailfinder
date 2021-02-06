from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Subscriber



class SubscriberForm(forms.ModelForm):
	class Meta:
		model=Subscriber
		fields=("email","name",)

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=225)
    last_name = forms.CharField(max_length=225)
    email = forms.EmailField()
    phone = forms.CharField(max_length=17, required=False)
    subject = forms.CharField(max_length=225)
    service = forms.CharField(max_length=225)
    messages = forms.CharField(widget=forms.TextInput(), max_length=800)

    def send_email(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        subject = self.cleaned_data.get('subject')
        service = self.cleaned_data.get('service')
        messages = self.cleaned_data.get('messages')

        rendered_message = render_to_string('Mobile/contact_email.html', {
           'name': f'{first_name} {last_name}',
           'email': email, 
           'phone': phone, 
           'subject': subject, 
           'service': service, 
           'messages': messages,
        })
        val = send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[settings.DEFAULT_COMPANY_NAME], fail_silently=fail)
        return True if val else False