#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.utils import timezone
from forum.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.comments.models import Comment


ROWS_PER_PAGE = 7

def showlist(request):
    pk = request.GET.get('category', 'notice')
    page = int(request.GET.get('page', 1))
    boardList = Paginator(Post.objects.filter(category__name = pk).order_by('-id'), ROWS_PER_PAGE)

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
    pk = int(request.GET.get('id', -1))
    category = request.GET.get('category', 'notice')
    postData = Post.objects.get(id=pk)
    Post.objects.filter(id = pk).update(hits = postData.hits + 1)

    return render(request, 'forum_view.html', {'postData':postData, 'user':request.user, 'category':category, 'path':request.get_full_path()})

def write_work(request):
    pk = request.GET.get('category', 'notice')

    return render(request, 'forum_write.html', {'category':pk, 'user':request.user})

@login_required
@csrf_exempt
def dowrite(request):
    category = request.POST.get('category', '')
    dr = Category.objects.get(name=category)

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

    url = '/forum?category=' + category
    return HttpResponseRedirect(url)

@login_required
def modify_work(request):
    pk = request.GET['id']
    category = request.GET['category']
    postData = Post.objects.get(id = pk)
    
    return render(request, 'forum_modify.html', {'postData':postData, 'user':request.user, 'category':category})

@login_required
@csrf_exempt
def domodify(request):
    pk = int(request.POST.get('id', -1))
    category = request.POST.get('category', '')
    postData = Post.objects.get(id = pk)
    
    postData.modified_on = timezone.now()
    postData.title = request.POST.get('title', 'No title')
    postData.text = request.POST.get('contents', '')
    
    dr = Category.objects.get(name = request.POST['category'])
    postData.category = dr
    postData.save()

    url = '/forum?category=' + category
    return HttpResponseRedirect(url)

@login_required
def delete_work(request):
    pk = int(request.GET.get('id',-1))
    category = request.GET.get('category', '')
    postData = Post.objects.get(id = pk)
    postData.delete()

    url = '/forum?category=' + category
    return HttpResponseRedirect(url)
