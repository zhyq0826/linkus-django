from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page


from views import * 

s='[\s\S]*'
s='^[a-z]([a-z0-9]*[-_\.]+?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2}'

urlpatterns = patterns('',
	(r'^register/$',register),
	(r'^active/(?P<email>[\s\S]*)/(?P<ck>[a-zA-Z0-9]*)/$',active),
	(r'^resetpassword/$',reset_pw_apply),
	(r'^resetpassword/(?P<id>\d+)/(?P<ck>[a-zA-Z0-9]*)/$',reset_pw),
	(r'^login/$',login),
	(r'^logout/$',logout),
)