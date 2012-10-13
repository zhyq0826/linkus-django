from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
from views import * 

s='[\s\S]*'
s='^[a-z]([a-z0-9]*[-_\.]+?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2}'

urlpatterns = patterns('',
	url(r'^(?P<id>[0-9a-zA-Z]{1,32})$',home),
)