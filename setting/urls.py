from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
from views import * 


isettingurl = patterns('',
	(r'^$',setting),
	(r'^profile/$',setting_profile),
	(r'^school/$',setting_school),
	(r'^account/$',setting_account),
	(r'^password/$',setting_password),
	(r'^getcollege/(?P<id>\d+)/$',getcollege),
    (r'^getschool/(?P<id>\d+)/$',getschool),
    (r'^url/$',setting_url),
    (r'^avatar/$',setting_avatar),
    (r'^avatar/crop/$',setting_crop_avatar),
)


iprofileurl = patterns('',
	(r'^$',profile),
)


urlpatterns = patterns('',
)