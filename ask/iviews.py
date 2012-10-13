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

#iask模板的前缀，即路径
i_ask_template_pefix='ask/i/'


def current_user_ask(request,template_name='ask/ask.html'):
	try:

		u = request.session['current_user']

		ask_answer_state = get_user_ask_answer_state(u.id)

		questions = get_limit_questions(u.id,0,5)

		answered_questions = get_limit_answered_questions(u.id,0,5)

		data={'questions':questions,'answered_questions':answered_questions,'ask_answer_state':ask_answer_state}
		return render_to_response(template_name,data,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


def current_user_asks(request,template_name='ask/asks.html'):
	try:
		u = request.session['current_user']


		paginator = Paginator(get_question_total_count(u.id),10)
		ask_answer_state = get_user_ask_answer_state(u.id)


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
		questions = get_limit_questions(u.id,page.start,page.end)
		data={'questions':questions,'ask_answer_state':ask_answer_state,'less_than_certain_size':less_than_certain_size,'page':page,'pages':pages}
		return render_to_response(template_name,data,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def ask(request,template_name=i_ask_template_pefix+'ask.html'):
	try:
		login_u = request.session['user']
		u = request.session['current_user']


		if u.id==login_u.id:
			pass
		else:
			return current_user_ask(request=request)


		paginator = Paginator(get_question_total_count(u.id),10)
		ask_answer_state = get_user_ask_answer_state(u.id)


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
		questions = get_limit_questions(u.id,page.start,page.end)
		data={'questions':questions,'ask_answer_state':ask_answer_state,'less_than_certain_size':less_than_certain_size,'page':page,'pages':pages}
		return render_to_response(template_name,data,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


	
def answer(request,template_name=i_ask_template_pefix+'answer.html'):
	try:
		u = request.session['current_user']

		login_u = request.session['user']

		if login_u.id==u.id:
			pass
		else:
			template_name='ask/answer.html'



		ask_answer_state = get_user_ask_answer_state(u.id)
		if ask_answer_state:
			paginator = Paginator(ask_answer_state.answer_count,20)
		else:
			paginator = Paginator(0,20)


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
		answered_questions = get_limit_answered_questions(u.id,page.start,page.end)
		data={'answered_questions':answered_questions,'ask_answer_state':ask_answer_state,'less_than_certain_size':less_than_certain_size,'page':page,'pages':pages}
		return render_to_response(template_name,data,context_instance=RequestContext(request))

		return render_to_response(template_name,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass




def question(request,template_name=i_ask_template_pefix+'question.html'):
	try:
		return render_to_response(template_name,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

