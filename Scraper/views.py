import time
import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, TemplateView

from .page_links import get_emails_from_page, get_emails_from_links
from .search_google import searchGoogle

from .models import EmailModel
from .forms import EmailCallForm
from .utils import clean_emails, email_validator


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
            new_dict['email'] = obj.email
            new_dict['domain'] = obj.domain
            new_dict['country'] = obj.country
            new_dict['status'] = str(random.randint(98,100))+'%'
            result_set.append(new_dict)
        
        return result_set
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        if request.is_ajax():
            # time.sleep(3)
            form = self.form_class(request.POST)
            if form.is_valid():
                formNum = form.cleaned_data.get('formNum')
                if formNum == 4:
                    # Get random emails
                    n = EmailModel.objects.count()
                    try:
                        list_nums = random.sample(list(range(n)), 600)
                    except ValueError:
                        return JsonResponse({'formNum':0}, status=400)

                    # Loop through listnums, get obj and add data to a dict
                    result_set = []
                    for i in list_nums:
                        try:
                            obj = EmailModel.objects.get(id=i)
                            new_dict = dict()
                            new_dict['email'] = obj.email
                            new_dict['domain'] = obj.domain
                            new_dict['country'] = obj.country
                            new_dict['status'] = str(random.randint(98,100))+'%'
                            result_set.append(new_dict)
                        except EmailModel.DoesNotExist:
                            pass
                elif formNum == 1:
                    email_names = form.cleaned_data.get('email_names')
                    email_names = email_names.split(' ')
                    email_set = []

                    # Loop through email_names, find all names that is similar to this
                    for i in email_names:
                        finds = EmailModel.objects.filter(name__icontains=i)
                        if finds.exists():
                            email_set = email_set+[i for i in finds]
                    
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

                        # Clean got emails
                        print(got_emails, 'This are the emails before cleaning')
                        clean_emails_list.extend(clean_emails(got_emails, i))
                        got_emails = []
                        
                        # print('\n\n',got_emails,'\n\n')
                    
                    # print(got_emails, 'This are the emails before cleaning')
                    
                    print(clean_emails_list, 'This are the clean emails')
                    
                    # All current database emails
                    db_emails = [i.email for i in domain_set]
                    
                    # Loop through searched emails to add to result set
                    for em in clean_emails_list:
                        # try:
                        if em not in db_emails:
                            # Validate the email using our master email validator
                            val = email_validator(em)
                            print(em, val, 'Validation status')
                            if val:
                                sp = em.split('@')
                                name = sp[0]
                                domain = sp[-1]

                                # Adding to database
                                obj = EmailModel.objects.create(email=em, name=name, domain=domain)
                                domain_set.append(obj)
                        # except:
                        #     pass

                    # Get serializable result set
                    result_set = self.get_serializable(domain_set)
                elif formNum == 3:
                    country = form.cleaned_data.get('country')
                    country_set = list(EmailModel.objects.filter(country__iexact=country))
                    
                    # Get serializable result set
                    result_set = self.get_serializable(country_set)

                return JsonResponse({'success':'no_errors', 'queryset':result_set}, status=200)

            # Show errors
            error_data = form.errors
            error_data['formNum'] = form.data.get('formNum')
            return JsonResponse(error_data, status=400)
        
        return render(request, self.template_name, context)
