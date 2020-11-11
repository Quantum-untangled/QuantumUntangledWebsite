from django.shortcuts import render

def index(request):
    return render(request, 'forum/index.html')

def sign_up(request):
    return render(request, 'forum/signup.html')