from django.urls import path,include
from . import views
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('user_settings/change-password/', views.ChangePassword.as_view(), name='change_password'),
    path("activate/<slug:uidb64>/<slug:token>/", views.activate_email, name="activate"),
    path('reset-password/', views.ResetPasswordFormPage.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.ResetPasswordVerify.as_view(), name='password_reset_confirm'),
]