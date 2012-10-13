from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
import views 



followurl=patterns('',
	(r'^(?P<id>\d+)/yes$',views.yesfollow),
	(r'^(?P<id>\d+)/no$',views.nofollow),
)

followerurl=patterns('',
	(r'^$',views.follower),
)

ifollowurl=patterns('',
	(r'^$',views.follow),
)