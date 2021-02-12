import time
import random

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, TemplateView

from .models import EmailModel
from .forms import EmailCallForm
# from .mixins import ManageSubscribe


class EmailFinder(FormView):
    template_name = 'Scraper/scraper.html'
    extra_context = {
        'title': 'Email finder'
    }
    form_class = EmailCallForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
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
                    list_nums = random.sample(list(range(n)), 600)

                    # Loop through listnums, get obj and add data to a dict
                    result_set = []
                    for i in list_nums:
                        obj = EmailModel.objects.get(pk=i)
                        new_dict = dict()
                        new_dict['email'] = obj.email
                        new_dict['domain'] = obj.domain
                        new_dict['country'] = obj.country
                        new_dict['status'] = random.randint(98,100)
                        result_set.append(new_dict)

                elif formNum == 1:
                    email_names = form.cleaned_data.get('email_names')
                return JsonResponse({'success':'no_errors', 'queryset':result_set}, status=200)

            # Show errors
            error_data = form.errors
            error_data['formNum'] = form.data.get('formNum')
            return JsonResponse(error_data, status=400)
        
        return render(request, self.template_name, context)
