from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .EmailBackEnd import EmailBackEnd
from django.contrib import messages


# from channels.auth import login

# Create your views here.


def sampleDemo(request):
    return render(request, 'demo.html')


def showLoginPage(request):
    return render(request, 'login_page.html')


def doLogin(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed')
    else:
        user = EmailBackEnd.authenticate(
            request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            return HttpResponseRedirect('/admin_home')
        else:
            messages.error(request, "Invalid Login")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse(f"{request.user.email} --> {request.user.user_type}")
    else:
        return HttpResponse("Please Login First")


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')
