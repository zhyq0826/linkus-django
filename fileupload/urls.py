from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
import views 


imageurl=patterns('',
	(r'^$',views.uploadimage),
)

