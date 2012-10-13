#-*- coding:utf-8 -*-
from django.http import HttpResponse,Http404
from django.template import Template,Context,RequestContext,TemplateDoesNotExist
from django.shortcuts import render_to_response,redirect
from forms import *
from linkusall.util import Paginator,EmptyPage

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

i_topic_template_prefix='topic/i/'




def topic(request,template_name=i_topic_template_prefix+'topic.html'):
	try:
		u = request.session['current_user']

		login_u = request.session['user']
		if u.id==login_u.id:
			pass
		else:
			template_name='topic/topic.html'

		total_count = get_topic_total_count(u.id)

		paginator = Paginator(total_count,20)

		page_number = request.GET.get('page')
		if page_number and page_number.isdigit():
			try:
				page = paginator.page(int(page_number))
				pages = paginator.calculate_display_pages(int(page_number))
			except EmptyPage:
				page = paginator.page(1)
				pages = paginator.calculate_display_pages(1)
		else:
			page = paginator.page(1)
			pages = paginator.calculate_display_pages(1)

		less_than_certain_size = paginator.check_less_than_certain_size()
		topics = get_limit_topics(u.id,page.start,page.end)
		data={'topics':topics,'total_count':total_count,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size}
		return render_to_response(template_name,data,context_instance=RequestContext(request))
	except Exception, e:
		raise Http404()
	else:
		pass
	finally:
		pass






def replied_topic(request,template_name=i_topic_template_prefix+'topic_replied.html'):
	try:
		return render_to_response(template_name)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

