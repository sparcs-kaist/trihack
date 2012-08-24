# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns(
    'forum.views',

	url(r'^$', views.showlist),
	url(r'^read/$', views.view),
	url(r'^write/$', views.write),
	url(r'^modify/$', views.modify),
	url(r'^delete/$', views.delete),
        url(r'^write_comment/$', views.write_comment),
        url(r'^delete_comment/$', views.delete_comment),
        url(r'^vote/$',views.vote),
)

