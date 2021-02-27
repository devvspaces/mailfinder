import base64
import re
from string import punctuation

from django import forms


class EmailCallForm(forms.Form):
    email_v = forms.EmailField(max_length=225, required=False)
    email_file = forms.CharField(widget=forms.TextInput ,required=False)
    company_name = forms.CharField(max_length=225, required=False)
    email_names=forms.CharField(max_length=255, required=False)
    domain_names=forms.CharField(max_length=300, required=False)
    country=forms.CharField(max_length=225, required=False)
    formNum=forms.IntegerField()
    len_eq=forms.IntegerField(required=False)


    def clean(self):
        cleaned_data = super(EmailCallForm, self).clean()
        email_v = cleaned_data.get('email_v')
        email_file = cleaned_data.get('email_file')
        formNum = cleaned_data.get('formNum')

        if formNum and int(formNum) == 4:
            if (email_v == '') and (email_file == ''):
                error = 'You should add either one of email or email file'
                self.add_error('email_v',error)
                self.add_error('email_file',error)
		
        return cleaned_data

    def clean_email_file(self):
        email_file = self.data.get('email_file')
        formNum = self.data.get('formNum')
        len_eq = self.data.get('len_eq')

        if formNum and int(formNum) == 4:
            if email_file:
                # This means a file was passed
                email_file+=('='*int(len_eq))
                # try:
                email_file=str(base64.b64decode(email_file))
                emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", email_file, re.I))
                if len(emails) < 1:
                    raise forms.ValidationError("There are no emails in this document")
                else:
                    return emails
                # except:
                #     raise forms.ValidationError("Your file could not be processed please make sure this file is a valid readable document")
		
        return email_file

    def clean_company_name(self):
        company_name = self.data.get('company_name')
        formNum = self.data.get('formNum')

        if formNum and int(formNum) == 1:
            for i in company_name:
                if i in punctuation:
                    raise forms.ValidationError("The company name you entered has a punctuation mark, it is not allowed")
		
        return company_name
    
    def clean_country(self):
        country = self.data.get('country')
        formNum = self.data.get('formNum')

        if formNum and int(formNum) == 1:
            if not country or country=='0':
                raise forms.ValidationError("Select a country")
		
        return country
    
    def clean_email_names(self):
        email_names = self.data.get('email_names')
        formNum = self.data.get('formNum')

        if formNum and int(formNum) == 1:
            for i in email_names:
                if i in punctuation:
                    raise forms.ValidationError("The name(s) you entered has a punctuation mark, it is not allowed")
		
        return email_names

    def clean_domain_names(self):
        domain_names = self.data.get('domain_names')
        formNum = self.data.get('formNum')

        if formNum and int(formNum) == 2:
            for i in domain_names:
                if i in punctuation.replace('.','').replace('-',''):
                    raise forms.ValidationError("The domain/s you entered is not allowed, enter only root domain names like hotmail.com or yahoo.com")
		
        return domain_names