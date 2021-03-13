from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.Landing.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('faq/', views.FAQ.as_view(), name='faq'),
    path('privacy-policy/', views.PrivacyPolicy.as_view(), name='privacy'),
    path('terms/', views.Terms.as_view(), name='terms'),
    path('contact-us/', views.Contact.as_view(), name='contact'),
    path('admin-conf/settings/', views.AdminConfig.as_view(), name='admin_conf'),
]