from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    (r'^register/$','accounts.views.register'),
    (r'^login/$','accounts.views.login_page'),
    (r'^logout/$','accounts.views.logout'),
	(r'^forum/$','forum.views.forum_page'),
    
    # Media Root
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media'}),
    # Examples:
    # url(r'^$', 'trihack.views.home', name='home'),
    # url(r'^trihack/', include('trihack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
