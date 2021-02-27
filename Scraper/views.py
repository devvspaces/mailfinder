import time
import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, TemplateView

from .page_links import get_emails_from_page, get_emails_from_links
from .search_google import searchGoogle

from .models import EmailModel, Company
from .forms import EmailCallForm
from .utils import clean_emails, email_validator, email_format

class EmailFinder(LoginRequiredMixin,FormView):
    template_name = 'Scraper/scraper.html'
    extra_context = {
        'title': 'Email finder'
    }
    form_class = EmailCallForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
    def get_serializable(self, email_set):
        # Loop through email set add data to a dict
        result_set = []
        for obj in email_set:
            new_dict = dict()
            # Call email validation
            obj.validate()
            new_dict['email'] = obj.email
            new_dict['domain'] = obj.domain
            new_dict['country'] = obj.country
            new_dict['status'] = obj.verified
            result_set.append(new_dict)
        
        return result_set
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        if request.is_ajax():
            # time.sleep(3)
            # Clone request
            cloned = request.POST.copy()
            for a,b in request.POST.items():
                if a.find('base64') != -1:
                    cloned['email_file'] = a.replace('base64,','')
            
            form = self.form_class(cloned)
            if form.is_valid():
                formNum = form.cleaned_data.get('formNum')
                print('Got here')
                if formNum == 1:
                    company_name = form.cleaned_data.get('company_name')
                    email_names = form.cleaned_data.get('email_names')
                    country = form.cleaned_data.get('country')
                    email_set = set()
                    if len(email_names.replace(' ','')) > 0:
                        email_names_list = email_names.split(' ')

                        # Loop through email_names, find all names that is similar to this
                        for i in email_names_list:
                            finds = EmailModel.objects.filter(name__icontains=i)
                            if finds.exists():
                                email_set.update(set([i for i in finds]))
                    
                    # Check if company name is already in database
                    saved_company = Company.objects.filter(name__iexact=company_name).first()
                    if saved_company:
                        saves = saved_company.emailmodel_set.all()
                        if saves.exists():
                            email_set.update(set([i for i in saves]))
                    else:
                        saved_company = Company.objects.create(name=company_name)
                    
                    # Search google for names and job title
                    email_names = email_names.split(' ')
                    searching_links = set()
                    for i in email_names:
                        searching_links.update(set(searchGoogle(f'{company_name} {i} email {country}')))
                    
                    # Get all emails crawled from links
                    got_emails = get_emails_from_links(searching_links)
                    print(got_emails)

                    # Make sure all emails are in correct format
                    got_emails = email_format(got_emails)

                    # All current database emails
                    # db_emails = [i.email for i in email_set]
                    
                    # Loop through searched emails to add to result set
                    for em in got_emails:
                        queryset = EmailModel.objects.filter(email__exact=em)
                        # try:
                        if queryset.exists() == False:
                            print('Started the new emails ', em)
                            # Validate the email using our master email validator
                            val = email_validator.email_validate(em)
                            print(em, val, 'Validation status')
                            sp = em.split('@')
                            name = sp[0]
                            domain = sp[-1]

                            # Adding to database
                            obj = EmailModel.objects.create(email=em, name=name, domain=domain, verified=val)
                            obj.company_names.add(saved_company)
                            email_set.add(obj)

                        # except:
                        #     pass
                    
                    # Get serializable result set
                    result_set = self.get_serializable(email_set)
                elif formNum == 2:
                    domain_names = form.cleaned_data.get('domain_names')
                    domain_names = domain_names.split(' ')
                    domain_set = []
                    got_emails = []
                    clean_emails_list = []

                    # Loop through domain_names, find all names that is similar to this
                    for i in domain_names:
                        finds = EmailModel.objects.filter(domain__iexact=i)
                        if finds.exists():
                            domain_set = domain_set+[i for i in finds]

                        # Searching google for results
                        google_results = searchGoogle(i+' email')
                        print(google_results, 'This are the links google_got')
                        got_emails = got_emails + get_emails_from_links(google_results)
                        print(got_emails, 'This is the google results email')

                        # Searching all pages in the site
                        got_emails = got_emails + get_emails_from_page(i)

                        # Check their format then Clean got emails
                        print(got_emails, 'This are the emails before cleaning')
                        clean_emails_list.extend(clean_emails(email_format(got_emails), i))
                        got_emails = []
                        
                        # print('\n\n',got_emails,'\n\n')
                    
                    # print(got_emails, 'This are the emails before cleaning')
                    
                    print(clean_emails_list, 'This are the clean emails')
                    
                    # All current database emails
                    # db_emails = [i.email for i in domain_set]
                    
                    # Loop through searched emails to add to result set
                    for em in clean_emails_list:
                        # try:
                        if EmailModel.objects.filter(email__exact=em).exists() == False:
                            print('Started the new emails ', em)
                            # Validate the email using our master email validator
                            val = email_validator.email_validate(em)
                            print(em, val, 'Validation status')
                            sp = em.split('@')
                            name = sp[0]
                            domain = sp[-1]

                            # Adding to database
                            obj = EmailModel.objects.create(email=em, name=name, domain=domain, verified=val)
                            domain_set.append(obj)
                        # except:
                        #     pass

                    # Get serializable result set
                    result_set = self.get_serializable(domain_set)
                elif formNum == 4:
                    email_v = form.cleaned_data.get('email_v')
                    email_file = form.cleaned_data.get('email_file')
                    email_set = []
                    got_emails = set()

                    if email_v:
                        got_emails.add(email_v)
                    if email_file:
                        print('Fgdfjaldfj')
                        got_emails.update(email_file)
                    
                    # Loop through searched emails to add to result set
                    for em in got_emails:
                        # try:
                        obj = EmailModel.objects.filter(email__exact=em)
                        if obj.exists():
                            email_obj = obj.first()
                            email_set.append(email_obj)
                        else:
                            # Validate the email using our master email validator
                            val = email_validator.email_validate(em)
                            sp = em.split('@')
                            name = sp[0]
                            domain = sp[-1]

                            # Adding to database
                            obj = EmailModel.objects.create(email=em, name=name, domain=domain, verified=val)
                            email_set.append(obj)
                        # except:
                        #     pass
                    
                    # Get serializable result set
                    result_set = self.get_serializable(email_set)

                return JsonResponse({'success':'no_errors', 'queryset':result_set}, status=200)

            # Show errors
            error_data = form.errors
            print(error_data)
            error_data['formNum'] = form.data.get('formNum')
            return JsonResponse(error_data, status=400)
        
        return render(request, self.template_name, context)
