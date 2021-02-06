from django.contrib import messages
# from django.core.paginator import Paginator
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
from django.views.generic import FormView, CreateView
from django.urls import reverse

from .models import Subscriber
from .forms import SubscriberForm, ContactForm
from .mixins import ManageSubscribe


class Landing(ManageSubscribe, CreateView):
    template_name = 'Mobile/index.html'
    extra_context = {
        'title': 'Home'
    }
    model = Subscriber
    fields = ('email','name',)
    success_url = '/'

class About(ManageSubscribe, CreateView):
    template_name = 'Mobile/about-us-1.html'
    extra_context = {
        'title': 'About Us'
    }
    model = Subscriber
    fields = ('email','name',)
    success_url = '/'

class FAQ(ManageSubscribe, CreateView):
    template_name = 'Mobile/faq.html'
    extra_context = {
        'title': 'FAQ'
    }
    model = Subscriber
    fields = ('email','name',)
    success_url = '/'

class PrivacyPolicy(ManageSubscribe, CreateView):
    template_name = 'Mobile/privacy-policy.html'
    extra_context = {
        'title': 'Privacy Policy'
    }
    model = Subscriber
    fields = ('email','name',)
    success_url = '/'

class Terms(ManageSubscribe, CreateView):
    template_name = 'Mobile/terms-and-conditions.html'
    extra_context = {
        'title': 'Terms and Conditions'
    }
    model = Subscriber
    fields = ('email','name',)
    success_url = '/'

class Contact(FormView):
    template_name = 'Mobile/contact-us.html'
    extra_context = {
        'title': 'Contact Us'
    }
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, form, *args, **kwargs):
        request = self.request
        