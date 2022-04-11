from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, sessions
from django.contrib.auth import authenticate, login, logout
from mysite import settings
from django.core.mail import send_mail
from django.contrib.sessions.models import Session

def home(request):
    return render(request, "authentication/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 != pass2:
            return render(request,"authentication/register.html",{
                'error_message':"Your passwords are mismatch",
            })
        if User.objects.filter(username=username): 
            return render(request,"authentication/register.html",{
                'error_message':"Username already exists! Please try other usernames or login!",
            })
        if len(username) > 20 or len(username) < 6:
            return render(request, "authentication/register.html",{
                'error_message' : "Username must be between 6 and 20 characters!",
            })
        if not pass1.isalnum():
            return render(request,"authentication/register.html",{
                'error_message':"Your password must contain both characters and numbers!",
            })
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("login")
    return render(request, "authentication/register.html")

def loginn(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if 'forgotpass' in request.POST:
            try:
                user = User.objects.get(username=username)
            except:
                return render(request, "authentication/login.html",{
                    'error_message' : "Please use a valid username to change password",
                })
            else:
                user = User.objects.get(username=username)
                user.set_password('a')
                user.save()
                messages.success(request, "Your account has been reset, you may login with the password 'a'")
                return redirect("login");
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            login(request, user)
            return redirect("home")
        else:
            return render(request, "authentication/login.html",{
                'error_message':"USERNAME OR PASSWORD IS INVALID",
            })
    return render(request, "authentication/login.html")
    

def logoutt(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            pass3 = request.POST['pass3']
            myuser = authenticate(username=request.user.username, password=pass1)
            if myuser is not None:
                if firstname != '':
                    myuser.first_name = firstname
                if lastname != '':
                    myuser.last_name = lastname
                if email != '':
                    myuser.email = email
                if pass2 != '':
                    if pass2 == pass3:
                        myuser.set_password(pass2)
                        myuser.save()
                        logout(request)
                        return redirect("login")
                if 'delete' in request.POST:
                    myuser.delete()
                    return redirect("login")
                myuser.save()
            else:
                if (username != '') or (firstname != '') or (lastname != '') or (email != '') or (pass2 != '') or (pass3 != '') or ('delete' in request.POST):
                    return render(request, "authentication/profile.html",{
                        'firstname' : request.user.first_name,
                        'lastname' : request.user.last_name,
                        'username' : request.user.username,
                        'email' : "Your email is not set" if request.user.email == '' else request.user.email,
                        'error_message' : 'You didn\'t type your password' if pass1 == '' else 'Your password is incorrect!',
                    })
        return render(request, "authentication/profile.html",{
            'firstname' : request.user.first_name,
            'lastname' : request.user.last_name,
            'username' : request.user.username,
            'email' : "Your email is not set" if request.user.email == '' else request.user.email,
        })
    else:
        return redirect("login")