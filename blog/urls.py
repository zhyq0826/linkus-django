from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
import iviews 
import views 
import aviews



iblogurl=patterns('',
	(r'^$',iviews.blog),
	(r'^/(?P<id>\d+)$',iviews.view_blog),	
)


blogurl=patterns('',
	(r'^create$',views.write_blog),
	(r'^edit/(?P<id>\d+)$',views.edit_blog),
	(r'^(?P<id>\d+)$',views.view_blog),
	(r'^save$',views.save_blog),
	(r'^comment$',views.comment_blog),
)

articleurl=patterns('',
	(r'^subject/(?P<id>\d+)/(?P<s>.*)',aviews.article_subject),
)

