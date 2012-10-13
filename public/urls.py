from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
import views




readurl=patterns('',
	(r'^$',views.reading),
)

icollegeurl=patterns('',
	(r'^$',views.icollege),
    (r'^topic$',views.icollege_topic),
    (r'^help$',views.icollege_help),
    (r'^ask$',views.icollege_ask),	
)

homeurl=patterns('',
	(r'^$',views.home),
)