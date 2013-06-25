from django.conf.urls import *
#from django.views.static import * 
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ktkanketa.views.index', name='home'),
	url(r'^survey_classification/$', 'ktkanketa.views.survey_classification'),
	#url(r'^vignete/(?P<vignetteNumber>\d{1}>)/$', 'ktkanketa.views.vignete'),
	#url(r'^vignete/$', 'ktkanketa.views.vignete'),
	url(r'^vignete/(\d+)/$', 'ktkanketa.views.vignete'),
	# url(r'^$', 'ktkanketa.views.home', name='home'),
    # url(r'^ktkanketa/', include('ktkanketa.foo.urls')),
	#(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
# media url hackery. le sigh. 
urlpatterns += patterns('',
    (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
     { 'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
)