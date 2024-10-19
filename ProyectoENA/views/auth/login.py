from django.shortcuts import render


def Login(request):
    return render(request, 'auth/login.html')