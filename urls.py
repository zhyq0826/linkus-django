from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings
import auth.urls
import home.urls
import setting.urls
import blog.urls
import topic.urls
import ask.urls
import follow.urls
import subject.urls
import public.urls
import fileupload.urls
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'linkusbeta1.views.home', name='home'),
    # url(r'^linkusbeta1/', include('linkusbeta1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


#js css image
urlpatterns +=patterns('',
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT,'show_indexes': False}),
)

#blog image
urlpatterns +=patterns('',
    (r'^img/blog/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT+'blog/','show_indexes': False}),
)

#avatar image
urlpatterns +=patterns('',
    (r'^img/avatar/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT+'avatar/','show_indexes': False}),
)

#avatar temp
urlpatterns +=patterns('',
    (r'^img/avatar/temp/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT+'avatar/temp/','show_indexes': False}),
)

#img 
urlpatterns +=patterns('',
    (r'^img/univ/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT+'img/','show_indexes': False}),
)


urlpatterns+=patterns('',
    url(r'^404/$',include(auth.urls.urlpatterns)),
)


urlpatterns +=patterns('',
    url(r'^$',index),
)


urlpatterns +=patterns('',
    url(r'^read/',include(public.urls.readurl)),
)



#auth 
urlpatterns +=patterns('',
	url(r'^accounts/',include(auth.urls.urlpatterns)),
)


#logined
urlpatterns +=patterns('',
	url(r'^people/',include(home.urls.urlpatterns)),
)

# urlpatterns +=patterns('',
#     url(r'^people/',include())
# )


#setting
urlpatterns +=patterns('',
    url(r'^setting/',include(setting.urls.isettingurl)),
)

#people blog
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/blog',include(blog.urls.iblogurl)),
)

#people topic
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/topic',include(topic.urls.itopicurl)),
)


#people ask
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/asks',include(ask.urls.iasksurl)),
)

#people ask
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/ask',include(ask.urls.iaskurl)),
)

#people question
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/question/',include(ask.urls.iquestionurl)),
)


#people answer
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/answer',include(ask.urls.ianswerurl)),
)

#people follow
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/follow',include(follow.urls.ifollowurl)),
)

#people follower
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/follower',include(follow.urls.followerurl)),
)


#people profile
urlpatterns +=patterns('',
    url(r'^people/([0-9a-zA-Z]{1,20})/profile',include(setting.urls.iprofileurl)),
)

#ask
urlpatterns +=patterns('',
    url(r'^ask/',include(ask.urls.askurl)),
)

#question
urlpatterns +=patterns('',
    url(r'^question/',include(ask.urls.questionurl)),
)


#answer
urlpatterns +=patterns('',
    url(r'^answer/',include(ask.urls.answerurl)),
)


#blog
urlpatterns +=patterns('',
    url(r'^blog/',include(blog.urls.blogurl)),
)


#article
urlpatterns +=patterns('',
    url(r'^article/',include(blog.urls.articleurl)),
)


#topic
urlpatterns +=patterns('',
    url(r'^topic/',include(topic.urls.topicurl)),
)

#follow
urlpatterns +=patterns('',
    url(r'^follow/',include(follow.urls.followurl)),
)


#tag
urlpatterns +=patterns('',
    url(r'^tag/',include(subject.urls.tagurl)),
)


#imageupload
urlpatterns +=patterns('',
    url(r'^image/blog/upload/',include(fileupload.urls.imageurl)),
)


#i college
urlpatterns +=patterns('',
    url(r'^i/college/',include(public.urls.icollegeurl)),
)


urlpatterns +=patterns('',
    url(r'^home/',include(public.urls.homeurl)),
)