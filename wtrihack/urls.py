from django.conf.urls import patterns, include, url
from wtrihack import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',views.loginpage),
    (r'^login/$',views.login),
    
    # Examples:
    # url(r'^$', 'trihack.views.home', name='home'),
    # url(r'^trihack/', include('trihack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
