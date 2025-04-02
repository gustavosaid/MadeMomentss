from django.shortcuts import render

def index(request):
    return render(request, 'login_user.html')


def criar_user(request):
    return render(request, 'criar_user.html')