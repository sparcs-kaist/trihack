#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.utils import timezone
from forum.models import *
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
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
        posts = sorted(Post.objects.filter(category__name = pk).annotate(Count('comment'))[:], key=lambda x: x.score, reverse=True)
        boardList = Paginator(posts, rowsPerPage)

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
    
    texts = []
    for row in boardList.page(page) :
        texts.append(row.text)

    shorttexts = map(lambda x: x[:200]+"..." if len(x)>200 else x,texts)
    articlelist = zip(boardList.page(page),shorttexts)
    return render(request, 'forum_list.html', {
        'articlelist':articlelist,
        'contacts':contacts, 
        'title':title, 
        'totalCnt':totalCnt, 
        'current_page':current_page, 
        'category':pk, 
        'boardlist':boardList,
        'criteria':criteria,
        })

def view(request):
    pk = int(request.GET.get('id', -1))
    category = request.GET.get('category', '')
    try:
        postData = Post.objects.filter(id = pk).annotate(Count('comment')).get()
        postData.hits=postData.hits+1
        postData.save()
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Invalid Post Number')

    return render(request, 'forum_view.html', {'postData':postData, 'category':category, 'path':request.get_full_path()})
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
def write(request):
    if request.method == 'GET':
        pk = request.GET.get('category', '')
        return render(request, 'forum_write.html', {'category':pk})
    else:
        if 'modify' in request.POST:
            return modify(request)

        category = request.POST.get('category', '')
        try:
            dr = Category.objects.get(name=category)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Invalid Category')

        # Create Post
        br = Post( title = request.POST.get('title', 'untitled'),
                created_on = timezone.now(),
                modified_on = timezone.now(),
                user = request.user,
                text = request.POST.get('contents', ''),
                hits = 0,
                category = dr)
        br.save()

        url = '/forum?category=' + category
        return HttpResponseRedirect(url)

@login_required
def modify(request):
    if request.method == 'GET':
        pk = int(request.GET.get('id', -1))
        category = request.GET.get('category', '')
        try:
            postData = Post.objects.get(id = pk)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Invalid Post')

        if postData.user != request.user:
            return HttpResponseBadRequest()
        return render(request, 'forum_write.html', {'postData':postData, 'category':category})

    else:
        pk = int(request.POST.get('id', -1))
        category = request.POST.get('category', '')
        try:
            postData = Post.objects.get(id = pk)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Invalid Post')

        if postData.user != request.user:
            return HttpResponseBadRequest()
        
        postData.modified_on = timezone.now()
        try:
            postData.title = request.POST['title']
            postData.text = request.POST['contents']
        except:
            return HttpResponseBadRequest('Invalid')
 
        try:
            dr = Category.objects.get(name=category)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Invalid Category')

        postData.category = dr
        postData.save()

        url = '/forum?category='+ category
        return HttpResponseRedirect(url)

@login_required
def delete(request):
    pk = int(request.GET.get('id', -1))
    category = request.GET.get('category', '')

    try:
        postData = Post.objects.get(id = pk)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Invalid Post')

    if postData.user != request.user:
        return HttpResponseBadReqeust()

    postData.delete()

    url = '/forum?category=' + category
    return HttpResponseRedirect(url)

@login_required
def write_comment(request):
    if request.method == 'POST':
        user = request.user
        post_id = int(request.POST.get('post', -1))
        content = request.POST.get('text','')
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist:
            return httpResponseBadRequest('Invalid Post')

        url = '/forum/read/?id=%d' % post_id
        new_comment = Comment(user=request.user, post=post, text=content)
        new_comment.save()

        return HttpResponseRedirect(url)
    else:
        return HttpResponse(json.dumps({
                'user': comment.user,
                'created_on': comment.created_on,
                'comment_id': comment.id,
                'comment_text': comment.text
            }))

@login_required
def delete_comment(request):
    comment_id = int(request.GET.get('comment', -1))

    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return httpResponseBadRequest('Invalid Approach')

    url = '/forum/read/?id=%d' % comment.post.id

    if request.user != comment.user:
        return HttpResponseBadRequest()

    comment.delete()
    
    return HttpResponse(json.dumps({
            'state': 'success'
        }))
