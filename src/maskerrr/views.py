from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib import messages

from mskr.forms import SignUpForm

def login_user(req):
    if not req.user.is_authenticated:
        if req.method == 'POST':
            username = req.POST['username']
            psw = req.POST['password']
            user = authenticate(req, username=username, password=psw)
            if user == None:
                messages.success(req, ("Loggin Error: either password is wrong or there is no such user..."))
                return redirect('login_user')
            else:
                login(req, user)
                messages.success(req, ("You've just been logged in"))
                return redirect('/')
        else:
            return render(req, 'login_user.html')
    else:
        return redirect('/')

def logout_user(req):
    logout(req)
    messages.success(req, ("You've been logged out"))
    return redirect('/')

def sign_up(req):
    if not req.user.is_authenticated:
        form = SignUpForm()
        if req.method == 'POST':
            form = SignUpForm(req.POST)
            if form.is_valid():
                form.save() #saving into DB that is related to the form
                username = form.cleaned_data['username']
                psw = form.cleaned_data['password1']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                user = authenticate(req, username=username, password=psw, first_name=first_name, 
                             last_name=last_name, email=email) #Она обычно возвращает объект пользователя, если учетные данные действительны,
                                #и None, если они не соответствуют требованиям аутентификации
                login(req, user)
                messages.success(req, ("Welcome to Musker!"))
                return redirect('/')
            else:
                messages.success(req, ('Error: your data is not valid, please, read the instruction'))
                return redirect('sign_up')
        else:
            return render(req, 'sign_up.html', {'form': form})
    else:
        messages.success(req, ("You've already been logged in"))
        return redirect('/')

