from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
import iviews
import views
import sviews

s='[\s\S]*'
s='^[a-z]([a-z0-9]*[-_\.]+?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2}'


ianswerurl=patterns('',
	(r'^$',iviews.answer),
)


iquestionurl=patterns('',
	# (r'^(?P<id>\d+)$',iviews.ask_detail),
	(r'^$',iviews.question),
)


iasksurl=patterns('',
	url(r'^$',iviews.current_user_asks),
)


iaskurl = patterns('',
	url(r'^$',iviews.ask),
)


askurl=patterns('',
	(r'^$',views.ask),
	(r'^create$',views.iask),
	(r'^save$',views.save_question),
	(r'^subject/(?P<id>\d+)/(?P<s>.*)',sviews.q_subject),
	(r'^hot$',sviews.q_hot),
	(r'^anonymity$',sviews.q_anonymity),
)


questionurl=patterns('',
	(r'^(?P<id>\d+)$',views.q_detail),
	(r'^(?P<id>\d+)/edit',views.edit_question),
	(r'^(?P<id>\d+)/close',views.close_question),
	(r'^(?P<id>\d+)/open',views.open_question),
)


answerurl=patterns('',
	(r'^add$',views.add_answer),
	(r'^save$',views.save_answer),
	(r'^(?P<id>\d+)/agree$',views.agree),
	(r'^(?P<id>\d+)/oppose$',views.oppose),
)




