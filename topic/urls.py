from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
import iviews
import views 


itopicurl = patterns('',
	(r'^$',iviews.topic),
	(r'^/replyed$',iviews.replied_topic),
)


topicurl = patterns('',
	(r'^$',views.topic),
	(r'^(?P<id>\d+)$',views.topic_detail),
	(r'^comment$',views.comment_topic),
	(r'^create$',views.new_topic),
	(r'^loadcomment/(?P<id>\d+)$',views.loadcomment),
)