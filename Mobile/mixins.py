from django.contrib import messages
from django.shortcuts import redirect

class ManageSubscribe:
    def form_valid(self, form, *args, **kwargs):
        name = form.cleaned_data.get('name')
        print('Code got here')
        messages.success(self.request, f'Thank you {name} for subscribing with us.')
        print(self.request)
        return super().form_valid(form)
