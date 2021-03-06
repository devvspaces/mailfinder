import time
import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, TemplateView

from .page_links import get_emails_from_page, get_emails_from_links
from .search_google import searchGoogle, searchBing

from .models import EmailModel, Company
from .forms import EmailCallForm
from .utils import clean_emails, email_validator, email_format
from .hunter_api import email_hunter

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
        # Get user obj
        user = self.request.user

        # Loop through email set add data to a dict
        result_set = []

        # Check if user has collected this email before
        user_emails = user.emails.all()

        # Set variable for new verified emails
        new_verified = 0
        
        for obj in email_set:
            new_dict = dict()

            # Check if this email obj is verified
            if obj.verified:
                if obj not in user_emails:
                    new_verified+=1
                    user.emails.add(obj)

            # Call email validation
            obj.validate()

            # Add values to dictionary
            new_dict['email'] = obj.email
            new_dict['domain'] = obj.domain
            print(obj, '\n\n')
            new_dict['country'] = obj.country
            new_dict['status'] = obj.verified
            result_set.append(new_dict)

        # Check if the user has enough credits for the new verified emails
        current_credit = user.credit_balance()
        if (current_credit > 0) and (current_credit >= new_verified):
            user.deduct_credit(new_verified)
            print('We deducted', new_verified)
            return result_set
        elif current_credit > 0:
            new_resultset=dict()
            # Since user credits is not enought but is more than zero, lets give the user all the email for the credits
            for a,b in zip(result_set, range(current_credit)):
                new_resultset[a] = result_set[a]
                user.deduct_credit(1)
                print('We deducted', new_verified)
            return new_resultset
                
        return 1001
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        if request.is_ajax():
            # Clone request
            cloned = request.POST.copy()
            for a,b in request.POST.items():
                if a.find('base64') != -1:
                    cloned['email_file'] = a.replace('base64,','')
            
            form = self.form_class(cloned)
            if form.is_valid():
                formNum = form.cleaned_data.get('formNum')
                if formNum == 1:
                    company_name = form.cleaned_data.get('company_name')
                    email_names = form.cleaned_data.get('email_names')
                    country = form.cleaned_data.get('country')
                    email_set = set()
                    searching_links = set()

                    # Getting the names passed to the form
                    names = email_names.split(' ')

                    # Getting the available emails from our database first
                    saved_company = Company.objects.filter(name__iexact=company_name).first()
                    if saved_company:
                        company_emails = saved_company.emailmodel_set.all()
                        if len(names) > 0:
                            for name in names:
                                email_set.update(set([i for i in company_emails.filter(name__iexact=name)]))
                    else:
                        saved_company = Company.objects.create(name=company_name)

                    # Call email_hunter email_finder
                    if len(names) == 2:
                        # If the user passed a fullname we want to find that email with email finder
                        hunter_emails = email_hunter.find_email(company_name, email_names)
                        if hunter_emails is not None:
                            email_set.add(hunter_emails)
                        else:
                            # This means no emails was found, we want to try our google search to find the email
                            searching_links.update(set(searchBing(f'{company_name} {email_names} contact email {country}', unique=False)))
                    else:
                        # If no names were passed or the names passed is less than or more than two we want to do hunter domain search
                        hunter_emails = email_hunter.domain_search(company_name=company_name)
                        if hunter_emails is not None:
                            email_set.update(set(hunter_emails))
                        else:
                            # Search google for names and job title
                            email_names = email_names.split(' ')
                            for i in email_names:
                                searching_links.update(set(searchBing(f'{company_name} {i} contact email {country}', unique=False)))
                    
                    if searching_links:
                        # Get all emails crawled from links
                        got_emails = get_emails_from_links(searching_links)

                        # Make sure all emails are in correct format
                        got_emails = email_format(got_emails)
                        
                        # Loop through searched emails to add to result set
                        for em in got_emails:
                            queryset = EmailModel.objects.filter(email__exact=em)
                            try:
                                if queryset.exists() == False:
                                    # Validate the email using our master email validator
                                    val = email_validator.email_validate(em)
                                    sp = em.split('@')
                                    name = sp[0]
                                    domain = sp[-1]

                                    # Adding to database
                                    obj = EmailModel.objects.create(email=em, name=name, domain=domain, verified=val)
                                    obj.company_names.add(saved_company)
                                    email_set.add(obj)
                            except:
                                pass

                    # Get serializable result set
                    result_set = self.get_serializable(email_set)
                elif formNum == 2:
                    domain_names = form.cleaned_data.get('domain_names')
                    domain_names = domain_names.split(' ')
                    domain_set = []
                    got_emails = []
                    clean_emails_list = []
                    failed_emails_list = []

                    # Loop through domain_names, find all names that is similar to this
                    for i in domain_names:
                        finds = EmailModel.objects.filter(domain__iexact=i)
                        if finds.exists():
                            domain_set = domain_set+[i for i in finds]
                        
                        # Lets try to use our email hunter to hunt emails
                        hunter_emails = email_hunter.domain_search(domain_name=i)
                        if hunter_emails is not None:
                            domain_set.extend(hunter_emails)
                        else:
                            # Searching google for results
                            google_results = searchGoogle(i+' contact email')
                            got_emails = got_emails + get_emails_from_links(google_results)

                            # Searching all pages in the site
                            got_emails = got_emails + get_emails_from_page(i)

                            # Check their format then Clean got emails and add failed emails to failed list for adding and verification
                            cleaned_emails, failed_emails = clean_emails(email_format(got_emails), i)
                            clean_emails_list.extend(cleaned_emails)
                            failed_emails_list.extend(failed_emails)

                            got_emails = []
                    
                    # Loop through searched emails to add to result set
                    for em in clean_emails_list:
                        try:
                            if EmailModel.objects.filter(email__exact=em).exists() == False:
                                # Validate the email using our master email validator
                                val = email_validator.email_validate(em)
                                sp = em.split('@')
                                name = sp[0]
                                domain = sp[-1]

                                # Adding to database
                                obj = EmailModel.objects.create(email=em, name=name, domain=domain, verified=val)
                                domain_set.append(obj)
                        except:
                            pass

                    # Get serializable result set
                    result_set = self.get_serializable(domain_set)

                    # Loop through failed email list
                    for i in failed_emails_list:
                        try:
                            val = email_validator.email_validate(i)
                            sp = i.split('@')
                            name = sp[0]
                            domain = sp[-1]

                            # Adding to database
                            EmailModel.objects.create(email=em, name=name, domain=domain, verified=val)
                        except:
                            pass
                elif formNum == 4:
                    email_v = form.cleaned_data.get('email_v')
                    email_file = form.cleaned_data.get('email_file')
                    email_set = []
                    got_emails = set()

                    if email_v:
                        got_emails.add(email_v)
                    if email_file:
                        got_emails.update(email_file)
                    
                    refined_emails = []

                    
                    # We want to reduce the emails we got here, to see if we have verified them before
                    for i in got_emails:
                        email_obj = EmailModel.objects.filter(email__exact=i)
                        if email_obj.exists():
                            email_obj2 = email_obj.first()
                            if email_obj2.needs_validation():
                                refined_emails.append(i)
                            else:
                                email_set.append(email_obj2)
                        else:
                            refined_emails.append(i)
                    
                    # Let's first verify this email with hunter api
                    hunter_emails = email_hunter.verify_emails(emails=got_emails)
                    if hunter_emails is not None:
                        email_set.extend(hunter_emails)
                    else:
                        # Loop through searched emails to add to result set
                        for em in got_emails:
                            # try:
                            obj = EmailModel.objects.filter(email__exact=em)
                            if obj.exists():
                                email_obj = obj.first()
                                email_obj.validate()
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

                # Check if result set is error codes
                if result_set == 1001:
                    error_message = 'You don\'t have enough credits in your account, buy more credits to get more emails'
                    return JsonResponse({'success':'no_errors', 'error_message':error_message}, status=200)
                return JsonResponse({'success':'no_errors', 'queryset':result_set}, status=200)

            # Show errors
            error_data = form.errors
            error_data['formNum'] = form.data.get('formNum')
            return JsonResponse(error_data, status=400)
        
        return render(request, self.template_name, context)
