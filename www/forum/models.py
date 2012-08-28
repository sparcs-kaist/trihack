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
    user = models.ForeignKey(User, null=False,related_name="posted_user")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    text = models.TextField(u"내용")
    category = models.ForeignKey(Category, null=False, verbose_name=u"게시판")
    hits = models.IntegerField(null=True, default=0, blank=True)
    voted = models.ManyToManyField(User,through="Vote")

    def __unicode__(self):
        return self.title

    @property
    def like(self):
        return Vote.objects.filter(user=self.user,post=self,like=True).count()
    @property
    def hate(self):
        return Vote.objects.filter(user=self.user,post=self,like=False).count()
    @property
    def score(self):
        return self.like-self.hate

class Comment(models.Model):
    user = models.ForeignKey(User, null=False)
    post = models.ForeignKey(Post, null=False)
    text = models.TextField(u"내용")
    created_on = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    user = models.ForeignKey(User, null=False,related_name="voted_user")
    post = models.ForeignKey(Post, null=False,related_name="voted_post")
    like = models.BooleanField() #True to like, False to hate
    class Meta:
        unique_together = (("user","post"))

class File(models.Model):
    name = models.TextField(u"파일 이름")
    post = models.ForeignKey(Post)
