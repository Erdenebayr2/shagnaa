from django.shortcuts import render, redirect
from .userForm import RegisterForm, AccountsForm
import hashlib
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import uuid

def user_login(request):
    if request.method == 'POST':
        username = str(request.POST['username']).split(sep="@")[0]
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")

            return redirect('index')
        else:
            messages.error(request, "Username or password in correct")
            return redirect('signin')
    elif request.method == 'GET':
        return render(request, "signin.html")
@login_required(login_url='signin')
def user_logout(request):
    auth.logout(request)
    return redirect('signin')

def user_register(request):
    if request.method == "POST":
        rform = RegisterForm(data=request.POST)
        aform = AccountsForm(data=request.POST)
        if rform.is_valid() and aform.is_valid():
            if rform["password"].value() == rform["repeat_password"].value():
                rform.instance.username = str(rform["email"].value()).split(sep="@")[0]
                user = rform.save()
                user.set_password(user.password)
                user.save()
                acc = aform.save(commit=False)
                acc.user = user
                if "pro_image" in request.FILES:
                    acc.pro_image = request.FILES["pro_image"]

                acc.save()
                messages.success(request, "Амжилттай бүртгэгдлээ.")
                return redirect('signin')
            else:
                messages.error(request, "Дахин шалгана уу?")
        return redirect("register")
    else:
        r = RegisterForm()
        a = AccountsForm()
        context = {
            "aform": a,
            "rform": r,
        }
        return render(request, "register.html", context)