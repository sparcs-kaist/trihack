# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import *

def loginpage(request) :
    return render_to_response("login.html",{})

def login(request) :
    if request.method =='POST':
        
    return HttpResponse("Success")
