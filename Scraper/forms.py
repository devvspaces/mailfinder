from string import punctuation

from django import forms


class EmailCallForm(forms.Form):
    job_title=forms.IntegerField(required=False)
    email_names=forms.CharField(max_length=255, required=False)
    domain_names=forms.CharField(max_length=300, required=False)
    country=forms.CharField(max_length=5, required=False)
    formNum=forms.IntegerField()

    # def clean_job_title(self):
    #     job_title = self.data.get('job_title')
    #     formNum = self.data.get('formNum')

    #     if formNum and int(formNum) == 1:
    #         for i in job_title:
    #             if i in punctuation:
    #                 raise forms.ValidationError("The Job title you entered has a punctuation mark, it is not allowed")
    #                 break
		
    #     return job_title
    
    def clean_email_names(self):
        email_names = self.data.get('email_names')
        formNum = self.data.get('formNum')

        if formNum and int(formNum) == 1:
            for i in email_names:
                if i in punctuation:
                    raise forms.ValidationError("The name(s) you entered has a punctuation mark, it is not allowed")
                    break
		
        return email_names

    def clean_domain_names(self):
        domain_names = self.data.get('domain_names')
        formNum = self.data.get('formNum')

        if formNum and int(formNum) == 2:
            for i in domain_names:
                if i in punctuation.replace('.','').replace('-',''):
                    raise forms.ValidationError("The domain/s you entered is not allowed, enter only root domain names like hotmail.com or yahoo.com")
                    break
		
        return domain_names