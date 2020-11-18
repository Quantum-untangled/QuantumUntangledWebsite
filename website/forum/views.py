from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout # alias to prevent overriding function with custom-defined logout function
from django.contrib.auth import login as django_login
from .forms import SignUpForm

def index(request):
    if not request.user.is_authenticated:
        return redirect(sign_up)

    return render(request, 'forum/index.html')

def sign_up(request):
    if request.user.is_authenticated:
        return redirect(index)

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            django_login(request, user)
            return redirect('/')

    return render(request, 'forum/login.html', {'register_form': form, 'view': 'register'})

def login(request):
    if request.user.is_authenticated:
        return redirect(index)

    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                return redirect('/')

    return render(request, 'forum/login.html', {'login_form': form, 'view': 'login'})

def logout(request):
    if request.method == "POST":
        django_logout(request)
    return redirect('/')