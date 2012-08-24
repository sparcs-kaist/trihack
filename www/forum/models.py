#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(u"제목", max_length=100)
    user = models.ForeignKey(User, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    text = models.TextField(u"내용")
    category = models.ForeignKey(Category, null=False, verbose_name=u"게시판")
    hits = models.IntegerField(null=True, default=0, blank=True)
    like = models.IntegerField(null=True, default=0, blank=True)
    hate = models.IntegerField(null=True, default=0, blank=True)
    commentnumber = models.IntegerField(null=True, default = 0, blank=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, null=False)
    post = models.ForeignKey(Post, null=False)
    text = models.TextField(u"내용")
    created_on = models.DateTimeField(auto_now_add=True)
