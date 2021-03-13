import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, TemplateView

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
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        form = self.form_class(request.POST)
        if form.is_valid():
            val = form.send_email()
            if val:
                messages.success(request, 'We have received your message and we will get back to you.')
                return redirect('contact')
            else:
                messages.warning(request, 'Your message was not sent please try again.')
        else:
            messages.warning(request, 'You did not properly fill the contact form.')
        
        context['form'] = form
        
        return render(request, self.template_name, context)


# This is just a function to make sure the values passed to the context keys matches what is required in our template
def readable(val):
    if val == True:
        return 1
    elif val == False:
        return 0
    return val

# As we have a readable function that helps the template to understand what is being done, we also have this function
# to make python understand what the template is doing
def to_python(val):
    if val == 1:
        return True
    elif val == 0:
        return False
    return val

class AdminConfig(TemplateView):
    template_name = 'Mobile/config.html'
    extra_context = {
        'title': 'Admin Settings'
    }
    form_class = ContactForm

    def get_config(self):
        # Read the configuration files and load them to the required fields
        with open(settings.CONFIG_LOCATION, 'r') as f:
            config = json.loads(f.read())

        return config

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context

        config = self.get_config()
        
        # Adding editable fields to the context
        for key,val in config.items():
            if key != 'GENERAL':
                for k,v in val[0].items():
                    context[k] = readable(v)
        
        return context
    
    def change_config(self, keyV, value):
        config = self.get_config()

        # Loop through every thing in the dictionary except the GENERAL key to change the value
        for key,val in config.items():
            if key != 'GENERAL':
                for k in val[0].keys():
                    if k == keyV:
                        config[key][0][k] = to_python(value)
                        break
                
        # Now we will try to write the new config file back
        data = json.dumps(config, indent=4)

        with open(settings.CONFIG_LOCATION,'w') as f:
            f.write(data)


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        # This is the dictionary with the required keys
        req_keys = dict()
        form_valid = True

        form = request.POST
        for key, val in form.items():
            if key != 'csrfmiddlewaretoken':
                req_keys[key] = int(val) if val.isdigit() else val
                if len(val) == 0:
                    context[key+'_ERROR'] = 'This field is required'
                    form_valid = False

        if form_valid:
            # We try to make the new config changes
            for k,v in req_keys.items():
                self.change_config(k,v)

            return redirect('admin_conf')
        else:
            messages.warning(request, 'You did not properly fill the contact form.')
        
        return render(request, self.template_name, context)