from django.contrib import admin
from .models import EmailModel, ScrapedLink


class EmailModelAdmin(admin.ModelAdmin):
	list_display=('email', 'name', 'domain', 'country', 'verified',)
	list_filter = ('verified','last_validated',)
	search_fields=['email','name','domain']

admin.site.register(EmailModel, EmailModelAdmin)
admin.site.register(ScrapedLink)