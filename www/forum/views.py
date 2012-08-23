# Create your views here.

from django.shortcuts import render_to_response, render
from forum.models import *
from django.views.decorators.csrf import csrf_exempt

def forum_page(request):
	return render(request, 'forum.html')
