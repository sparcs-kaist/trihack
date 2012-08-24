# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns(
    'forum.views',

	url(r'^$', views.showlist),
	url(r'^read/$', views.view_work),
	url(r'^write/$', views.write_work),
	url(r'^dowrite/$', views.dowrite),
	url(r'^modify/$', views.modify_work),
	url(r'^domodify/$', views.domodify),
	url(r'^delete/$', views.delete_work),
        url(r'^write_comment/$', views.write_comment),
        url(r'^delete_comment/$', views.delete_comment),
)

