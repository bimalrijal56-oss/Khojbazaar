from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
# Create your views here.

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfully')
            return redirect('login')
        else:
            messages.error(request,'failed to create account')
            return render(request,'auth/register.html',{'form':form})

    context = {
        'form':UserCreationForm
    }
    return render(request,'auth/register.html',context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
           username = request.POST.get('username')
           password = request.POST.get('password')
           user = authenticate(request,username=username,password=password)
           if user is not None:
               login(request,user)
               if user.is_staff:
                messages.success(request,f"welcome {user.username}!\n You Are Logged In.")
                return redirect('all-product')
               elif user.is_active:
                 messages.success(request,f"welcome {user.username}!\n You Are Logged In.")
                 return redirect('/')
           else:
               messages.error(request,'Invalid username or password')
               return render(request,'auth/login.html',{'form':form})
    context = {
        'form':LoginForm
    }
    return render(request,'auth/login.html',context)


def user_logout(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('/')