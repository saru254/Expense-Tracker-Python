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

#Login and index function
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

#Other functions
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

#Updating Profile
def profile_update(request, id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            user.userprofile.Savings = request.POST["Savings"]
            user.userprofile.income = request.POST["income"]
            user.userprofile.profession = request.POST["profession"]
            user.userprofile.save()
            user.save()
            return redirect("/profile")
    return redirect("/home")

#signup, login, logout backend

def handleSignup(request):
    if request.method == 'POST':

        uname = request.POST["uname"]
        fname = request.POST["fname"]
        lname = request.POST['lname']
        email = request.POST["email"]
        profession = request.POST['profession']
        Savings = request.POST['Savings']
        income = request.POST['income']
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        profile = UserProfile(Savings = Savings,
                              profession = profession,
                              income = income)
        if request.method =='POST':
            try:
                user_exists = User.objects.get(username = request.POST['uname'])
                messages.error(request, "Username already taken")
                return redirect("/register")
            except User.DoesNotExist:
                if len(uname)>15:
                    messages.error(request, "Username must be max 15 characters")

                    return redirect("/register")
                if not uname.isalnum():
                    messages.error(request, "Username should only contain letters and numbers, Please try again")
                    return redirect("/register")
                if pass1 != pass2:
                    messages.error(request, "Password do not match, Please try again")
                    return redirect("/register")
                user = User.objects.create_user(uname, email,pass1)
                user.first_name = fname
                user.last_name = lname
                user.email = email
                #profile save

                user.save()

                profile.user = user
                profile.save()

                messages.success(request, "Your account has been successfully created")