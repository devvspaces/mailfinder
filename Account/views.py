from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, CreateView, TemplateView
from django.urls import reverse
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from .models import User
from .forms import UserRegisterForm, LoginForm
from .tokens import acount_confirm_token



def verification_message(request, user):
	site=get_current_site(request)
	uid=urlsafe_base64_encode(force_bytes(user.pk))
	token=acount_confirm_token.make_token(user)
	message=render_to_string("Account/activation_email.html",{
		"user": user.first_name,
		"uid": uid,
		"token": token,
		"domain": site.domain,
		'from': settings.DEFAULT_FROM_EMAIL
	})
	return message


class Register(FormView):
    template_name = 'Account/signup.html'
    extra_context = {
        'title': 'Register'
    }
    form_class = UserRegisterForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            subject=f"MailFinder Verification"
            message = verification_message(request, user)
            sent=user.email_user(subject,message)
            messages.success(request, f'You account is successfully created. A link was sent to your email {user.email}, use the link to verify you account.')
            return redirect('login')
        else:
            messages.warning(request, 'You did not properly fill the sign up form.')
        
        context['form'] = form
        
        return render(request, self.template_name, context)


class Login(FormView):
    template_name = 'Account/login.html'
    extra_context = {
        'title': 'Login'
    }
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name}')
                return redirect('home')
            else:
                messages.warning(request, 'Your email is not yet verified.')
                return redirect('login')
        else:
            messages.warning(request, 'You did not properly fill the sign up form.')
        
        context['form'] = form
        
        return render(request, self.template_name, context)


def activate_email(request, uidb64, token):
	try:
		uid=force_text(urlsafe_base64_decode(uidb64))
		user=User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user=None
	if user!=None and acount_confirm_token.check_token(user,token):
		user.active=True
		user.save()

		messages.success(request,f'{user.email}, your email is now verified successfully, you can now login')
		return redirect('login')
	else:
		messages.warning(request, 'This link is invalid')
		return render(request, "User/login.html")