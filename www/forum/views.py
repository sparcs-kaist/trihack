#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.utils import timezone
from forum.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.comments.models import Comment


rowsPerPage = 7

def showlist(request):
	if 'category' in request.GET:
		pk = request.GET['category']
	else:
		pk = 'notice'

	boardList = Paginator(Post.objects.filter(category__name = pk).order_by('-id'), rowsPerPage)

	if 'page' in request.GET:
		page = request.GET.get('page')
	else:
		page = 1
# paging
	try:
		contacts = boardList.page(page)
	except PageNotAnInteger:
		contatcs = boardList.page(1)
	except EmptyPage:
		contacts = boardList.page(boardList.num_pages)	

	if pk == 'notice':
		title = "NOTICE"
	else:
		title = "FREE BOARD"

	totalCnt = Post.objects.filter(category__name = pk).count()
	current_page = page

	return render(request, 'forum_list.html', {'boardList':boardList.page(page), 'contacts':contacts, 'title':title, 'totalCnt':totalCnt, 'current_page':current_page, 'category':pk, 'user':request.user})


def view_work(request):
	pk = request.GET['id']
	category = request.GET['category']
	postData = Post.objects.get(id = pk)

	Post.objects.filter(id = pk).update(hits = postData.hits + 1)
	return render(request, 'forum_view.html', {'postData':postData, 'user':request.user, 'category':category, 'path':request.get_full_path()})


def write_work(request):
	pk = request.GET['category']
	return render(request, 'forum_write.html', {'category':pk, 'user':request.user})


@csrf_exempt
def dowrite(request):
	dr = Category.objects.get( name = request.POST['category'])
	# Create Post
	br = Post( title = request.POST['title'],
			created_on = timezone.now(),
			modified_on = timezone.now(),
			user = request.user,
			text = request.POST['contents'],
			hits = 0,
			like = 0,
			hate = 0,
			commentnumber = 0,
			category = dr)
	br.save()

	url = '/forum?category=' + request.POST['category']
	return HttpResponseRedirect(url)


def modify_work(request):
	pk = request.GET['id']
	category = request.GET['category']
	postData = Post.objects.get(id = pk)
	
	return render(request, 'forum_modify.html', {'postData':postData, 'user':request.user, 'category':category})


@csrf_exempt
def domodify(request):
	pk = request.POST['id']
	category = request.POST['category']
	postData = Post.objects.get(id = pk)
	
	postData.modified_on = timezone.now()
	postData.title = request.POST['title']
	postData.text = request.POST['contents']
	
	dr = Category.objects.get( name = request.POST['category'])
	postData.category = dr
	postData.save()

	url = '/forum?category='+ category
	return HttpResponseRedirect(url)


def delete_work(request):
	pk = request.GET['id']
	category = request.GET['category']
	postData = Post.objects.get(id = pk)
	postData.delete()

	url = '/forum?category=' + category
	return HttpResponseRedirect(url)
