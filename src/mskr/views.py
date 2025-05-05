from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfPicForm, UserUpdateForm

from chat.models import *

def home(req):
    if req.user.is_authenticated:
        form = MeepForm(req.POST or None)
        if req.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = req.user
                meep.save()
                messages.success(req, ('Your Meep has been posted'))

        meeps = Meep.objects.all().order_by("-created")
        return render(req, 'home.html', {"meeps": meeps, "form": form})
    else:
        return render(req, 'home.html')

def profile_list(req):
    user = req.user
    if user.is_authenticated:
        profiles = Profile.objects.exclude(id=user.id)
        return render(req, 'profile_list.html',
                    {'profiles': profiles})
    else:
        messages.success(req, ('You must be logged in!'))
        return redirect('/')

def profile(req, pk):
    if req.user.is_authenticated:
        meeps = Meep.objects.filter(user=User.objects.get(id=pk))
        profile = Profile.objects.get(user_id=pk)
        if req.method == 'POST':
            curr_user = req.user.profile
            if profile != curr_user:
                if req.POST['follow'] == 'unfollow':
                    curr_user.follows.remove(profile)
                elif req.POST['follow'] == 'follow':
                    curr_user.follows.add(profile)
                curr_user.save()
        return render(req, 'profile.html', {'profile': profile, 'meeps': meeps})
    else:
        messages.success(req, ('You must be logged in!'))
        return redirect('home')
    
def update_user(req):
    if req.user.is_authenticated:
        user = req.user
        profile = Profile.objects.get(user=user)

        form = UserUpdateForm(req.POST or None, instance=user)
        pic_form = ProfPicForm(req.POST or None, req.FILES or None, instance=profile)

        if req.method == 'POST':
            if form.is_valid() and pic_form.is_valid():
                form.save()
                pic_form.save()
                login(req, user)
                messages.success(req, ('Your profile has been updated!'))
                return redirect('/')
            else:
                messages.success(req, ('There is sth wrong('))
                print(form.errors)  # Выведет ошибки формы пользователя
                print(pic_form.errors)  # Выведет ошибки формы профиля
                return render(req, 'update_user.html', {'form': form, 'pic_form': pic_form})
            
        else:
            return render(req, 'update_user.html', {'form': form, 'pic_form': pic_form})
    
    else:
        messages.success(req, ('You must be logged in!'))
        return redirect('/')

def meep_likes(req, pk):
    if req.user.is_authenticated:
        meep = get_object_or_404(Meep,id=pk)
        if meep.likes.filter(id=req.user.id):
            meep.likes.remove(req.user)
        else:
            meep.likes.add(req.user)
        return redirect('/')
    else:
        messages.success(req, ('You must be logged in!'))
        return redirect('/')

def meep(req, pk):
    meepp = Meep.objects.get(id=pk)
    return render(req, 'meep.html', {'meep': meepp})

def delete_meep(req, pk):
    if req.user.is_authenticated:
        meep = get_object_or_404(Meep,id=pk)
        
        if meep.user.username == req.user.username:
            meep.delete()
            messages.success(req, ("U've just deleted this meep"))
            return redirect('/')
        else:
            messages.success(req, ("Wtf ngga it's not ur meep"))
            return redirect('/')
    else:
        messages.success(req, ('You must be logged in!'))
        return redirect('/')

def search(req):
    if req.user.is_authenticated:
        searched = req.GET['search']
        meeps = Meep.objects.filter(body__icontains=searched)  # Фильтрация по body
        return render(req, 'search_results.html', {'meeps': meeps, 'search': searched})
    else:
        messages.success(req, ('You must be logged in!'))
        return redirect('/')
