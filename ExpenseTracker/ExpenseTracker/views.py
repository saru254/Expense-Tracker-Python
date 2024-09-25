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
