"""ExpenseTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path ('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('handleSignup/', views.handleSignup, name = 'handleSignup'),
    path('handlelogin/', views.handlelogin, name = 'handlelogin'),
    path('handleLogout/', views.handleLogout, name = 'handleLogout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "home/reset_password.html"), name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "home/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/token>/', auth_views.PasswordResetConfirmView.as_view(template_name= "hoem/password_reset_form.html"), name = 'password_reset_done'),
    path('reset_password_complete/', auth_views.PasswordResetView.as_view(template_name= "home/password_reset_done.html"), name = 'password_reset_complete'),

    path('addmoney/', views.addmoney, name='addmoney'),

    path('addmoney_submission/', views.addmoney_submission, name = 'addmoney_submission'),

    path('charts/', views.charts,name = 'charts'),
    path('tables/', views.tables, name = 'tables'),
    path('expense_edit/<int:id>', views.expense_edit, name = 'expense_edit'),
    path('<int:id>/addmoney_update/', views.addmoney_update, name = "addmoney_update"),

    path('expense_delete/<int:id>', views.expense_Delete, name = 'expense_delete'),
    
]