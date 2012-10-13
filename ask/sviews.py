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
from linkusall.subject.models import get_subjects,get_c_tags,get_c_subjects,get_one_subject

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 


def q_subject(request,template_name='public/ask_subject.html',id=None,s=None):
	if id and id.isdigit() and s:
		s = decode_data(str(s))
		one = get_one_subject(int(id))
		if one:
			if one.subject==s:
				page_number = request.GET.get('page')
				paginator = Paginator(get_some_subject_question_count(int(id)),10)

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
				
				questions = get_questions_by_subject(int(id),page.start,page.end)
				subjects = get_subjects()
				data={'questions':questions,'one':one,'subjects':subjects}
				return render_to_response(template_name,data,context_instance=RequestContext(request))
			else:
				raise Http404()
		else:
			raise Http404()
	else:
		raise Http404()


def q_hot(request,template_name='public/ask_hot.html'):
	page_number = request.GET.get('page')
	paginator = Paginator(get_question_total_count(),20)

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
	
	questions = get_limit_questions(start=page.start,end=page.end,order='-answer_count')
	subjects = get_subjects()
	data={'questions':questions,'hot_current':'ana_focus_current','subjects':subjects,'page':page}
	return render_to_response(template_name,data,context_instance=RequestContext(request))


def q_anonymity(request,template_name='public/ask_anonymity.html'):
	page_number = request.GET.get('page')
	paginator = Paginator(get_question_total_count(),20)

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
	
	questions = get_limit_anonymity_questions(start=page.start,end=page.end)
	subjects = get_subjects()
	data={'questions':questions,'ano_current':'ana_focus_current','subjects':subjects,'page':page}
	return render_to_response(template_name,data,context_instance=RequestContext(request))