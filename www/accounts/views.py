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
    redirection = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirection = request.POST.get('next')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if redirection=='' :
                    return HttpResponseRedirect('/')
                else :
                    return HttpResponseRedirect(redirection)
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    if request.GET :
        redirection = request.GET.get('next')

    return render(request, 'login.html', {'username': username,'state': state,'next':redirection})
  
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    teamE = emailE = contactE = members_name1E = members_name2E = members_name3E = members_university1E = members_university2E = members_university3E = countryE = ''
    team = email = contact = members_name1 = members_name2 = members_name3 = members_university1 = members_university2 = members_university3 = country = ''
    error = False
    
    expertise = []
    expertise_list = ['web', 'ios', 'android', 'ui/ux design', 'front-end', 'back-end', 'systems', 'security', 'database']
    expertise_check = [0 for i in expertise_list]
    
    country_list = ['KOREA', 'JAPAN', 'CHINA']
    country_check = [0 for i in country_list]
    
    if request.POST:
        team = request.POST.get('team')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        expertise = request.POST.getlist('expertise')

        members_name1 = request.POST.get('members_name1')
        members_name2 = request.POST.get('members_name2')
        members_name3 = request.POST.get('members_name3')

        members_university1 = request.POST.get('members_university1')
        members_university2 = request.POST.get('members_university2')
        members_university3 = request.POST.get('members_university3')
       
        country = request.POST.get('country')

        if team == None or team.strip() == '' :
            teamE = "There is no team name"
            error = True
        if email == None or email.strip() == '' :
            emailE = "There is no Email address"
            error = True
        elif not validateEmail(email.strip()) :
            emailE = "Invalid Email Address"
            error = True
        if contact == None or contact.strip() == '':
            contactE = "There is no contact"
            error = True
        
        for i in range(len(expertise_list)):
            if expertise_list[i] in expertise:
                expertise_check[i] = 1

        for i in range(len(country_list)):
            if country_list[i] == country:
                country_check[i] = 1
        
        if members_name1 == None or members_name1.strip() == '':
            members_name1E = "There is no first member name"
            error = True
        
        if members_university1 == None or members_university1.strip() == '':
            members_university1E = "There is no first member university"
            error = True

        if country == None:
            countryE = 'There is no country'
            error = True
        
        if not error :
	    filepath = os.path.join(os.path.dirname(__file__), '../result.txt')
            f = open(filepath,"a+")
            f.write(' / '.join([team,email,contact,str(expertise_list),members_name1,members_name2,members_name3,members_university1,members_university2,members_university3,country])+"\n")
            f.close()
            return render(request,'register_success.html',{})
        
    return render(request,'register.html',
            {
            'team':team, 'teamE':teamE,
            'email':email, 'emailE':emailE,
            'contact':contact, 'contactE':contactE,
            'expertise_check': expertise_check,
            'members_name1':members_name1, 
            'members_name1E':members_name1E, 
            'members_name2':members_name2, 
            'members_name2E':members_name2E, 
            'members_name3':members_name3, 
            'members_name3E':members_name3E, 
            'members_university1':members_university1, 
            'members_university1E':members_university1E, 
            'members_university2':members_university2, 
            'members_university2E':members_university2E, 
            'members_university3':members_university3, 
            'members_university3E':members_university3E, 
            'country': country,
            'countryE': countryE,
            'country_check': country_check,
            })

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@[a-zA-Z0-9]+[a-zA-Z0-9\\-\\.]*\\.([a-zA-Z]{2,3}|[0-9]{1,3})$", email) != None:
            return True
        return False

def changelanguage(request, lang):
    request.session['django_language'] = lang
    return HttpResponseRedirect('/about/')
