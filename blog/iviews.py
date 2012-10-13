# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext,Template, Context
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
from forms import *
from models import *
import re

from django.http import Http404,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError

from linkusall.util import Paginator,EmptyPage
from linkusall.subject.models import get_subjects,get_c_tags,get_c_subjects

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

i_blog_template_prefix='blog/i/'

#分页 当分页参数中有分类时，进行分类分页，否则进行普通的分页
def blog(request,template_name=i_blog_template_prefix+'blog.html'):
	try:
		u = request.session['current_user']

		login_u = request.session['user']

		if u.id ==login_u.id:
			pass
		else:
			template_name='blog/blog.html'

		total_count = get_article_total_count(u.id)

		# request.user = u
        #如果请求要求分类，则进行分类
		paginator = Paginator(get_article_total_count(u.id),20)


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
		articles = get_limit_articles(u.id,page.start,page.end)
		

		data={'articles':articles,'total_count':total_count,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size}
		return render_to_response(template_name,data,context_instance=RequestContext(request))
		
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


def view_blog(request,template_name='blog/i/blog_view.html',id=None):
	try:

		u = request.session['current_user']

		tags=[]
		subjects=[]
	
		if id and id.isdigit():
			id = int(id)
			article =  get_article(int(id))
			
			if not article:
				raise Http404()

			author = u

			page_number = request.GET.get('page')
			comment_count = get_article_comments_count(article.id)
			paginator = Paginator(comment_count,10)

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

			if article.tag:
				tags = get_c_tags(article.tag)

			if article.subject:
				subjects = get_c_subjects(article.subject)

			comments = get_limit_comments(article.id,page.start,page.end)
			next_article = get_user_next_article(u.id,id)
			prev_article = get_user_prev_article(u.id,id)

			data={'article':article,'author':author,'comment_count':comment_count,'tags':tags,'subjects':subjects,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size,'comments':comments,'next_article':next_article,'prev_article':prev_article}
			return render_to_response(template_name,data,context_instance=RequestContext(request))
		else:
			raise Http404()
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass