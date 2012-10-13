from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
import views

s='[\s\S]*'
s='^[a-z]([a-z0-9]*[-_\.]+?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2}'


tagurl=patterns('',
	(r'^$',views.query_tag),
)
