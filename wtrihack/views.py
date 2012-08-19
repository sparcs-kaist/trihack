# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_page(request) :
    state = ''
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render(request, 'login.html', {'username': username,'state': state})
  
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
