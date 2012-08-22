# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import *
from django.views.decorators.csrf import csrf_exempt
import re

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

def register(request):
    nameT = "Name"
    teamT = "Team name"
    emailT = "Email"
    locationT = 'Location' 
    nameE = teamE = emailE = locationE =''
    name = team = email = location = ''
    checked = None
    error = False
    if request.POST:
        name = request.POST.get('entry.0.single')
        team = request.POST.get('entry.3.single')
        email = request.POST.get('entry.1.single')
        location = request.POST.get('entry.2.group')
        if name.strip() == '' :
            nameE = "There is no name" 
            nameT = ""
            error = True
        if team.strip() == '' :
            teamE = "There is no team name"
            teamT = ""
            error = True
        if email.strip() == '' :
            emailE = "There is no Email address"
            emailT =""
            error = True
        elif not validateEmail(email.strip()) :
            emailE = "Invalid Email Address"
            emailT = "" 
            error = True
        if location == None or  location.strip() == '':
            locationE = "There is no Location information" 
            locationT = ""
            error = True
       
        if not error :
            return render(request,'register_success.html',{})
        
    return render(request,'register.html',
            {'nameT':nameT,
            'teamT':teamT,
            'emailT':emailT,
            'locationT':locationT,
            'nameE':nameE,
            'teamE':teamE,
            'emailE':emailE,
            'locationE':locationE,
            'name':name,
            'team':team,
            'email':email,
            'location':location})

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@[a-zA-Z0-9]+[a-zA-Z0-9\\-\\.]*\\.([a-zA-Z]{2,3}|[0-9]{1,3})$", email) != None:
            return True
        return False
