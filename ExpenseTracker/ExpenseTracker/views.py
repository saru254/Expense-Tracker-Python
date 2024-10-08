#importing modules

from django.shortcuts import render, HttpResponse, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, logout # type: ignore
from django.contrib.auth import login as dj_login # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Addmoney_info, UserProfile
from django.contrib.sessions.models import Session # type: ignore
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # type: ignore
from django.db.models import Sum # type: ignore
from django.http import JsonResponse # type: ignore
import datetime
from django.utils import timezone # type: ignore

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
                return redirect("/")
            else:
                return HttpResponse('404 - NOT FOUND')
            return redirect('/login')
        def handlelogin(request):
            if request.method == 'POST':

                loginuname = request.POST["loginuname"]
                loginpassword1 = request.POST["loginpassword1"]
                user = authenticate(username =loginuname, 
                                    password = loginpassword1)
                
                if user is not None:
                    dj_login(request, user)
                    request.session['is_logged'] = True
                    user = request.user.id
                    request.session ["user_id"] = user
                    messages.success(request, "Successfully logged in")
                    return redirect('/index')
                else:
                    messages.error(request, "Invalid Credentials, Please try again")
                    return redirect("/")
                return HttpResponse('404 - NOT FOUND')
            def handleLogout(request):
                del request.session['is_logged']
                del request.session["user_id"]
                logout(request)
                messages.success(request, "Successfully logged out")
                return redirect('home')

#Add money form and add money update backend

def addmoney_submission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id = user_id)

            Addmoney_info1 = Addmoney_info.objects.filter(user = user1).order_by('-Date')
            add_money = request.POST["add_money"]
            quantity = request.POST["quantity"]
            Date = request.POST["Date"]
            Category = request.POST["Category"]
            add = Addmoney_info(user = user1,
                                add_money = add_money,
                                quantity = quantity,
                                Date = Date,
                                Category =Category)
            add.save()
            paginator = Paginator(Addmoney_info1, 4)
            page_number = request.GET.get('page')
            page_obj = Paginator.get_page(paginator, page_number)
            context = {
                'page_obj' : page_obj
            }
            return render(request, 'home/index.html'.context)
        return redirect('/index')
    def addmoney_update(request, id):
        if request.session.has_key('is_logged'):
            if request.method == "POST":
                add = Addmoney_info.objects.get(id=id)
                add.add_money = request.POST["add_money"]
                add.quantity = request.POST["quantity"]
                add.Date = request.POST["Date"]
                add.Category = request.POST["Category"]
                add.save()
                return redirect("/index")
            return redirect("/home")
        

#Expense Edit and Expense Delete Backend
def expense_edit(request, id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
    return render(request, 'home/expense_edit.html', {'addmoney_info': addmoney_info})
    return redirect("/home")

def expense_delete(request, id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        addmoney_info.delete()
        return redirect("/index")
    return redirect("/home")

#monthly,weekly,yearly expense backend.

def expense_month(request):
    todays_date = datetime.date.today()
    one_month_ago = todays_date-datetime.timedelta(days=30)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)

    addmoney= Addmoney_info.objects.filter(user=user1, Date__gte = one_month_ago, Date__lte=todays_date)

    finalrep = {}

    def get_Category(addmoney_info):
        return addmoney_info.Category
    Category_list = list(set(map(get_Category,addmoney)))
     
    def get_expense_category_amount(Category,add_money): 
        quantity = 0
        filtered_by_category = addmoney.filter(Category = Category, add_money="Expense")
        for item in filtered_by_category:
            quantity+=item.quantity
            return quantity
        for x in addmoney:
            for y in Category_list:
                finalrep[y] = get_expense_category_amount(y, "Expense")
                return JsonResponse ({'expense_category_data': finalrep}, safe=False)
    
    def stats(request):
        if request.session.has_key('is_logged'):
            todays_date = datetime.date.today()
            one_month_ago = todays_date-datetime.timedelta(days=30)
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)

            addmoney_info = Addmoney_info.objects.filter(user=user1,Date__gte=one_month_ago, Date__lte=todays_date)
            sum = 0
            for i in addmoney_info:
                if i.add_money == 'Expense':
                    sum = sum+i.quantity
            addmoney_info.sum = sum

            sum1 = 0
            for i in addmoney_info:
                if i.add_money == 'Income':
                    sum1 = sum1+i.quantity
            addmoney_info.sum1 = sum1
            x = user1.userprofile.Savings+addmoney_info.sum1 - addmoney_info.sum
            y = user1.userprofile.Savings+addmoney_info.sum1 - addmoney_info.sum

            if x < 0:
                messages.warning(request, 'Your expense exceeded your savings')
                x = 0
            
            if x >0:
                y = 0
            addmoney_info.x = abs(x)
            addmoney_info.y = abs(y)
            return render(request, 'home/stats.html',{'addmoney':addmoney_info})
    
def expense_week(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1,
                                             Date__gte = one_week_ago,
                                             Date__lte =todays_date)
    finalrep = {}

    def get_Category(addmoney_info):
        return addmoney_info.Category
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0
        filtered_by_category = addmoney.filter(Category = Category,
                                              add_money="Expense")
        
        for item in filtered_by_category:
            quantity+=item.quantity
            return quantity
        
        for x in addmoney:
            for y in Category_list:
                finalrep[y] = get_expense_category_amount(y, "Expense")
                return JsonResponse({'expense_category_data': finalrep}, safe= False)

def weekly(request):
    if request.session.has_key('is_logged'):
        todays_date = datetime.date.today()
        one_week_ago = todays_date-datetime.timedelta(days=7)
        user_id = request.session["user_id"]
        user1 = User.objcts.get(id=user_id)

        addmoney_info= Addmoney_info.objects.filter(user =user1,
                                                    Date__gte =one_week_ago,
                                                    Date__lte=todays_date)
        sum = 0
        for i in addmoney_info:
            if i.add_money == 'Expense':
                sum = sum+i.quantity
        addmoney_info.sum = sum

        sum1 = 0

        for i in addmoney_info:
            if i.add_money == 'Income':
                sum1 = sum1.i.quantity
        addmoney_info.sum1 = sum1

        x =user1.userprofile.Savings + addmoney_info.sum1 - addmoney_info.sum
        y =user1.userprofile.Savinga + addmoney_info.sum1 - addmoney_info.sum

        if x>0:
            messages.warning(request, 'Your expense exceeded your savings')
            x = 0
        if x> 0:
            y = 0
        addmoney_info.x = abs(x)
        addmoney_info.y = abs(y)   
    return render(request, 'home/weekly.html', 
                  {'addmoney_info':addmoney_info})   

def check(request):
    if request.method == 'POST':
        user_exists =User.objects.filter(email=request.POST['email'])
        messages.error(request, "Email not registered, TRY AGAIN!!")
        return redirect("/reset/password")

def info_year(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date - datetime.timedelta(days = 30 * 12)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user =user1,
                                        Date__gte=one_week_ago,
                                        Date__lte=todays_date)
    finalrep ={}
    def get_Category(addmoney_info):
        return addmoney_info.Category
    Category_list = list(set(map(get_Category,addmoney)))
    def get_expense_category_amount(Category,add_money):
        quantity = 0
        filtered_by_category = addmoney.filter(Category = Category,
                                               add_money ='Expense')
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity
    for x in addmoney:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y, "Expense")
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def info(request):
    return render(request, 'home/info.html')
