from django import forms
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

from .models import User



class ResetPasswordValidateEmailForm(forms.Form):
	email=forms.CharField(help_text="Enter your Mailfinder email")

	def clean_email(self):
		email = self.data.get('email')
		validate_email(email)
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist as e:
			raise forms.ValidationError("Email user matched no MailFinder account")
		
		return email

class ProfileForm(forms.Form):
	id = forms.IntegerField()
	first_name = forms.CharField(max_length=225)
	last_name = forms.CharField(max_length=225)
	email = forms.EmailField(max_length=255)
	phone = forms.CharField(max_length=20)
	gender = forms.IntegerField()
	country = forms.CharField(max_length=3)
	def clean(self):
		cleaned_data = super(ProfileForm, self).clean()

		# Get the user object
		id = cleaned_data.get('id')
		user = get_object_or_404(User, id=id)

		email = cleaned_data.get('email')
		phone = cleaned_data.get('phone')
		gender = int(cleaned_data.get('gender'))

		if gender not in [1,2]:
			self.add_error('gender', 'Invalid gender')

		email_exist = User.objects.filter(email=email).exclude(id=id).exists()
		if email_exist:
			self.add_error('email', 'This email has already been used')
		
		phone_exist = User.objects.filter(phone=phone).exclude(id=id).exists()
		if phone_exist:
			self.add_error('email', 'This phone number has already been used')
		
		return cleaned_data
	
	def save(self, commit=True):
		cleaned_data = self.clean()
		# Get the user object
		id = cleaned_data.get('id')
		user = get_object_or_404(User, id=id)

		email = cleaned_data.get('email')
		phone = cleaned_data.get('phone')
		first_name = cleaned_data.get('first_name')
		last_name = cleaned_data.get('last_name')
		gender = cleaned_data.get('gender')
		country = cleaned_data.get('country')

		user.email = email
		user.phone = phone
		user.first_name = first_name
		user.last_name = last_name
		user.gender = gender
		user.country = country

		if commit:
			user = user.save()
		
		return user

class ForgetPasswordForm(forms.Form):
	user_pk = forms.CharField(max_length=255)
	new_password=forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form__input'}),
		help_text=password_validation.password_validators_help_text_html()
	)
	confirm_password=forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form__input'}),
		help_text='Must be similar to first password to pass verification'
	)

	# Cleaning password one to check if all validations are met
	def clean_new_password(self):
		ps1=self.cleaned_data.get("new_password")
		password_validation.validate_password(ps1,None)
		return ps1

	"""Override clean on password2 level to compare similarities of password"""
	def clean_confirm_password(self):
		ps1=self.cleaned_data.get("new_password")
		ps2=self.cleaned_data.get("confirm_password")
		if (ps1 and ps2) and (ps1 != ps2):
			raise forms.ValidationError("The passwords does not match")
		return ps2

	def save(self, commit=True):
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		user.set_password(self.cleaned_data.get("new_password"))
		if commit:
			user.save()
		return user


class ChangePasswordForm(forms.Form):
	user_pk = forms.IntegerField()
	current_password=forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form__input'}),
		help_text='Enter your current password here'
	)
	new_password=forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form__input'}),
		help_text=password_validation.password_validators_help_text_html()
	)

	# Cleaning old password to check if provided password matches user password
	def clean_current_password(self):
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		password = self.cleaned_data.get('current_password')
		if not user.check_password(password):
			raise forms.ValidationError('Your password is not correct')
		return password

	# Cleaning password one to check if all validations are met
	def clean_new_password(self):
		ps1=self.cleaned_data.get("new_password")
		password_validation.validate_password(ps1,None)
		return ps1

	def save(self, commit=True):
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		user.set_password(self.cleaned_data.get("new_password"))
		if commit:
			user.save()
		return user


class ChangePassword(forms.ModelForm):
	password_old=forms.CharField(label="Old password",widget=forms.PasswordInput)
	password1=forms.CharField(label="New password",widget=forms.PasswordInput)
	password2=forms.CharField(label="Confirm password",widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=("password_old","password1","password2",)
	
	def clean_password2(self):
		#Validating if password1 and 2 are correct
		password1=self.cleaned_data.get("password1")
		password2=self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("New passwords do not match")
		return password2

# class UserUpdateProfile(forms.ModelForm):
# 	class Meta:
# 		model=Profile
# 		fields=("image",'username','id_photo','address','country','state','city',)

class LoginForm(forms.Form):
	email=forms.EmailField()
	password=forms.CharField(widget=forms.PasswordInput())
	def clean(self):
		data=super(LoginForm, self).clean()
		email = data.get('email')
		password = data.get('password')
		validate_email(email)
		try:
			user = User.objects.get(email=email)
			if not user.check_password(password):
				self.add_error('password', forms.ValidationError('Your password is incorrect'))
		except User.DoesNotExist as e:
			self.add_error('email', forms.ValidationError("This account does not exist"))
		return data

class UserRegisterForm(forms.ModelForm):
	password=forms.CharField(label="Password",
							widget=forms.PasswordInput,
							min_length=8,
							help_text=password_validation.password_validators_help_text_html())
	password2=forms.CharField(label="Confirm password",
							widget=forms.PasswordInput,
							help_text='Must be similar to first password to pass verification')
	class Meta:
		model=User
		fields=("email",'phone',"first_name","last_name",'gender','country',"password","password2",)
	# Cleaning password one to check if all validations are met
	def clean_password(self):
		ps1=self.cleaned_data.get("password")
		password_validation.validate_password(ps1,None)
		return ps1
	"""Override clean on password2 level to compare similarities of password"""
	def clean_password2(self):
		ps1=self.cleaned_data.get("password")
		ps2=self.cleaned_data.get("password2")
		if (ps1 and ps2) and (ps1 != ps2):
			raise forms.ValidationError("The passwords does not match")
		return ps2
	""" Override the default save method to use set_password method to convert text to hashed """
	def save(self, commit=True):
		user=super(UserRegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data.get("password"))
		if commit:
			user.save()
		return user

class UserUpdateForm(forms.ModelForm):
	password=ReadOnlyPasswordHashField()
	class Meta:
		model=User
		fields=("email","phone",'gender','country','first_name','last_name',"password","active","staff","admin",)
		def clean_password(self):
			# Regardless of what the user provides, return the initial value.
			# This is done here, rather than on the field, because the
			# field does not have access to the initial value
			return self.initial["password"]