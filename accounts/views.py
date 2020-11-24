from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# Create your views here.


def home(request):
    return render(request,'accounts/dashboard.html')


def regular(request):
    return render(request,'accounts/regular.html')


def company(request):
    return render(request,'accounts/company.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Access denied.')
            return redirect('login')                

    else:
        return render(request,'accounts/login.html')


def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        user_type = request.POST['user_type']

        if password.strip() != password_confirmation.strip():
            messages.info(request, 'Password does not match.')
            return redirect('register')
        if User.objects.filter(email = email ).count() > 0:
            messages.info(request, 'Email already registered.')
            return redirect('register')
        user = User.objects.create_user(
            email,
            fname = fname,
            lname = lname,
            password = password,
            type = user_type            
        )
        
        user.save()
        return redirect('login')
    else:
        return render(request,'accounts/register.html')        