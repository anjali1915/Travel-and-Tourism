"""
URL configuration for BharatYatra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SendMail
from BharatYatra import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/login/', lambda request: redirect('/login/')),
    path('login/', views.login_view, name="login_page"),
    path('register/', views.user_register, name='register'),
    #password reset views
    path('password_reset/', SendMail.as_view(), name="password_reset"),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    #location
    path('travel/', views.travel_view, name="explore_nearby_places"),
    #contact page
    path('contact/', views.contact_page, name="contact"),
    path('Post_User/', views.Post, name="post"),
    path('social/', views.social, name="social"),
    path('profile/', views.Profile_view, name="profile_view"),
    path('Profile_Edit/', views.Profile_Edit, name="profile_edit"),

    path('logout/', views.logout, name="logout")
]
