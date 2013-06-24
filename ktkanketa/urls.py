from django.conf.urls import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ktkanketa.views.index', name='home'),
	url(r'^survey_classification/$', 'ktkanketa.views.survey_classification'),
	#url(r'^vignete/(?P<vignetteNumber>\d{1}>)/$', 'ktkanketa.views.vignete'),
	#url(r'^vignete/$', 'ktkanketa.views.vignete'),
	url(r'^vignete/(\d+)/$', 'ktkanketa.views.vignete'),
	# url(r'^$', 'ktkanketa.views.home', name='home'),
    # url(r'^ktkanketa/', include('ktkanketa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
