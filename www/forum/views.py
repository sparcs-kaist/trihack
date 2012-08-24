#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.utils import timezone
from forum.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Count
import json
rowsPerPage = 7

def showlist(request):
    pk = request.GET.get('category', 'notice')
    criteria = request.GET.get('criteria', 'new')

    if criteria == 'new':
        boardList = Paginator(Post.objects.filter(category__name = pk).order_by('-id').annotate(Count('comment')), rowsPerPage)
    else:
        boardList = Paginator(Post.objects.filter(category__name = pk).extra(
            select={"score":'like - hate'},
            order_by = ('-score',)
            ).annotate(Count('comment')), rowsPerPage)

    page = int(request.GET.get('page', 1))

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
    
    texts=[]
    for row in boardList.page(page) :
        texts.append(row.text)

    shorttexts= []
    likes = [] 
    hates = []
    for i in boardList.page(page) :
        likes.append(i.getLike())
        hates.append(i.getHate())
   
    shorttexts=map(lambda x: x[:200]+"..." if len(x)>200 else x,texts)
    articlelist = zip(boardList.page(page),shorttexts,likes,hates)
    return render(request, 'forum_list.html', {
        'articlelist':articlelist,
        'contacts':contacts, 
        'title':title, 
        'totalCnt':totalCnt, 
        'current_page':current_page, 
        'category':pk, 
        'user':request.user,
        'boardlist':boardList,
        'criteria':criteria,
        })

@csrf_exempt
def view_work(request):
    pk = int(request.GET.get('id', -1))
    category = request.GET.get('category', '')
    postData = Post.objects.filter(id = pk).annotate(Count('comment')).get()
    postData.hits=postData.hits+1
    postData.save()
#        Post.objects.filter(id = pk).update(hits=postData.hits + 1)
    return render(request, 'forum_view.html', {'postData':postData, 'user':request.user, 'category':category, 'path':request.get_full_path(),'like':postData.getLike(),'hate':postData.getHate()})

@login_required
def vote(request):
    if request.method == 'POST': 
        pk = int(request.POST.get('id', -1))
        category = request.POST.get('category', '')
        postData = Post.objects.get(id = pk)

        if 'like' in request.POST:
            try:
                Vote(user=request.user,post=postData,like=True).save()
            except IntegrityError :
                return HttpResponse(json.dumps({'state':'falied'}))
        elif 'hate' in request.POST:
            try:
                Vote(user=request.user,post=postData,like=False).save()	
            except IntegrityError:
                return HttpResponse(json.dumps({'state':'failed'}))

        url = "/forum/read/?id=" + str(pk) + "&category=" + category
        return HttpResponse(json.dumps(
            {'state':'success'}
            ))
    else :
        return HttpResponseBadRequest()
@login_required
def write_work(request):
    pk = request.GET.get('category', '')
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
            category = dr)
    br.save()

    url = '/forum?category=' + category
    return HttpResponseRedirect(url)

@login_required
def modify_work(request):
    pk = int(request.GET.get('id', -1))
    category = request.GET['category']
    postData = Post.objects.get(id = pk)
    if postData.user != request.user:
        return HttpResponseBadRequest()
    return render(request, 'forum_modify.html', {'postData':postData, 'user':request.user, 'category':category})


@login_required
@csrf_exempt
def domodify(request):
    pk = int(request.POST.get('id', -1))
    category = request.POST.get('category', '')
    postData = Post.objects.get(id=pk)
    if postData.user != request.user:
        return HttpResponseBadRequest()
    
    postData.modified_on = timezone.now()
    postData.title = request.POST['title']
    postData.text = request.POST['contents']
    
    dr = Category.objects.get(name=category)
    postData.category = dr
    postData.save()

    url = '/forum?category='+ category
    return HttpResponseRedirect(url)

@login_required
def delete_work(request):
    pk = int(request.GET.get('id', -1))
    category = request.GET.get('category', '')
    postData = Post.objects.get(id = pk)
    if postData.user != request.user:
        return HttpResponseBadReqeust()

    postData.delete()

    url = '/forum?category=' + category
    return HttpResponseRedirect(url)

@login_required
def write_comment(request):
    user = request.user
    post_id = int(request.POST.get('post', -1))
    content = request.POST.get('text','')
    post = Post.objects.get(pk=post_id)
    url = '/forum/read/?id=%d' % post_id
    new_comment = Comment(user=request.user, post=post, text=content)
    new_comment.save()


    return HttpResponseRedirect(url)

@login_required
def delete_comment(request):
    user = request.user
    comment_id = int(request.GET.get('comment', -1))

    comment = Comment.objects.get(id=comment_id)
    url = '/forum/read/?id=%d' % comment.post.id

    if request.user != comment.user:
        return HttpResponseBadRequest()

    comment.delete()
    
    return HttpResponseRedirect(url)
