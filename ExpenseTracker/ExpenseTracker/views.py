#importing modules

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from .models import Addmoney_info, UserProfile
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
import datetime
from django.utils import timezone

def home(request):
    if request.session.has_key('is_logged'):
        return redirect('/index')
    return render (request, 'home/login.html')

def index(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)

        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info, 4)
        page_number = request.GET.get('page')

        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'page_obj' : page_obj
        }

        return render(request, 'home/index.html', context)
    return redirect('home')

def addmoney(request):
    return render(request, 'hoe/addmoney.html')

def profile(request):
    if request.session.has_key('is_logged'):
        return render (request, 'home/profile.html')
    return redirect('/home')

def profile_edit(request,id):
    if request.session.has_key('is_logged'):
        add = User.objects.get(id=id)
        return render(request, 'home/profile_edit.html',{'add':add})
    return redirect("/home")

def profile_update(request, id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            user.userprofile.Savings = request.POST["Savings"]
            user.userprofile.income = request.POST["income"]
            