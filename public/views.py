# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext,Template, Context
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
import re

from django.http import Http404,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError

from linkusall.util import Paginator,EmptyPage
from linkusall.subject.models import get_subjects
from linkusall.blog.models import get_articles_by_comment_recommended,get_article_total_count,get_i_college_article_count,get_articles_by_i_college
from linkusall.topic.models import get_i_college_topic_count,get_i_college_limit_topics
from linkusall.ask.models import get_i_college_question_count,get_i_college_limit_questions

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 



def reading(request,template_name='public/read.html'):

	page_number = request.GET.get('page')
	paginator = Paginator(get_article_total_count(),10)

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
	
	articles = get_articles_by_comment_recommended(page.start,page.end)
	subjects = get_subjects()
	data={'articles':articles,'all_current':'ana_focus_current','subjects':subjects,'page':page}
	return render_to_response(template_name,data,context_instance=RequestContext(request))




def icollege(request,template_name="public/icollege3.html"):
	u = request.session['user']
	# page_number = request.GET.get('page')
	# paginator = Paginator(get_i_college_article_count(u.id),5)

	# if page_number and page_number.isdigit():
	# 	try:
	# 		page = paginator.page(int(page_number))
	# 		pages = paginator.calculate_display_pages(int(page_number))
	# 	except EmptyPage:
	# 		page = paginator.page(1)
	# 		pages = paginator.calculate_display_pages(1)
	# else:
	# 	page = paginator.page(1)
	# 	pages = paginator.calculate_display_pages(1)
	
	articles = get_articles_by_i_college(u.id,0,5)
	topics = get_i_college_limit_topics(u.id,0,5)
	questions = get_i_college_limit_questions(u.id,0,20)
	subjects = get_subjects()
	data={'articles':articles,'topics':topics,'questions':questions,'all_current':'ana_focus_current','subjects':subjects}
	return render_to_response(template_name,data,context_instance=RequestContext(request))


def icollege_blog(request,template_name="public/icollege_blog.html"):
	return render_to_response(template_name,context_instance=RequestContext(request))



def icollege_topic(request,template_name="public/icollege_topic.html"):
	u = request.session['user']
	total_count = get_i_college_topic_count(u.id)

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
	topics = get_i_college_limit_topics(u.id,start=page.start,end=page.end)
	data={'topics':topics,'topic_current':'ana_focus_current','total_count':total_count,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size}
	return render_to_response(template_name,data,context_instance=RequestContext(request))



def icollege_ask(request,template_name="public/icollege_ask.html"):
	u = request.session['user']
	page_number = request.GET.get('page')
	paginator = Paginator(get_i_college_question_count(u.id),20)

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
	
	questions = get_i_college_limit_questions(u.id,start=page.start,end=page.end)
	subjects = get_subjects()
	data={'questions':questions,'ask_current':'ana_focus_current','subjects':subjects,'page':page}
	return render_to_response(template_name,data,context_instance=RequestContext(request))

def icollege_help(request,template_name="public/icollege_help.html"):
	data={'help_current':'ana_focus_current'}
	return render_to_response(template_name,data,context_instance=RequestContext(request))



def home(request,template_name='public/home.html'):
	return render_to_response(template_name,context_instance=RequestContext(request))