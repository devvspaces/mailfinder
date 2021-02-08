from django.urls import path,include
from . import views
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path("activate/<slug:uidb64>/<slug:token>/", views.activate_email, name="activate"),
]