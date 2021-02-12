from django.urls import path,include

from . import views
urlpatterns = [
    path('email-finder/', views.EmailFinder.as_view(), name='email_finder'),
]