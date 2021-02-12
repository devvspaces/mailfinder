from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Mobile.urls')),
    path('accounts/',include('Account.urls')),
    path('secured/',include('Scraper.urls')),
]
