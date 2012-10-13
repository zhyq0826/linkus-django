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

#ask模板的前缀，即路径
ask_template_pefix="ask/"

def q_detail(request,template_name=ask_template_pefix+'detail.html',id=None):
	try:
		u = request.session['user']

		tag_list=[]
		subject_list=[]

		if id and id.isdigit():
			question = get_question(int(id))
			if question:
				paginator=Paginator(get_question_answer_count(question['q'].id),15)
				page_number = request.GET.get('page')

				if question['q'].tag:
					tag_list = get_c_tags(question['q'].tag)

				if question['q'].subject:
					subject_list = get_c_subjects(question['q'].subject)

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

				user_answer=check_user_answer_state(question['q'].id,u.id)
				less_than_certain_size = paginator.check_less_than_certain_size()
				answers = get_limit_answers(question['q'].id,page.start,page.end)
				data={'q':question,'user_answer':user_answer,'answers':answers,'tags':tag_list,'subjects':subject_list}

				return render_to_response(template_name,data,context_instance=RequestContext(request))
		else:
			raise Http404()
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass



def ask(request,template_name='public/ask.html'):
	try:
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
		
		questions = get_limit_questions(start=page.start,end=page.end)
		subjects = get_subjects()
		data={'questions':questions,'all_current':'ana_focus_current','subjects':subjects,'page':page}
		return render_to_response(template_name,data,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


def answer(request,template_name='ask/answer.html'):
	try:
		return render_to_response(template_name,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


def iask(request,template_name=ask_template_pefix+'iask.html'):
	try:

		u = request.session['user']

		subjects =get_subjects()



		if request.method=='GET':
			form = QuestionForm(auto_id='%s')
			return render_to_response(template_name,{'form':form,'subjects':subjects},context_instance=RequestContext(request))
		else:
			form = QuestionForm(request.POST,auto_id='%s')
			tag_list = request.POST.getlist('tag_list')
			subject_list = request.POST.getlist('subject_list')

			if form.is_valid():
				form.save(u.id,tag_list,subject_list)
				return redirect('/ask/')
			else:
				return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass


def question(request,template_name='ask/question.html'):
	try:
		return render_to_response(template_name,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def close_question(request,id=None):
	if request.is_ajax():
		if id and id.isdigit():
			u = request.session['user']
			if close(u.id,int(id)):
				return HttpResponse('{status:true}')
			else:
				return HttpResponse('{status:true}')
		else:
			raise Http404()
	else:
		raise Http404()

def open_question(request,id=None):
	if request.is_ajax():
		if id and id.isdigit():
			u = request.session['user']
			if close(u.id,int(id),'open'):
				return HttpResponse('{status:true}')
			else:
				return HttpResponse('{status:true}')
		else:
			raise Http404()
	else:
		raise Http404()


def save_question(request):
	u = request.session['user']

	if request.method=='POST':
		form = QuestionForm(request.POST,auto_id='%s')
		tag_list = request.POST.getlist('tag_list')
		subject_list = request.POST.getlist('subject_list')

		if form.is_valid():
			form.update(u.id,tag_list,subject_list)
			return redirect('/ask/')
		else:
			return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
	else:
		raise Http404()

#todo 
def edit_question(request,template_name='ask/iaskedit.html',id=None):
	u = request.session['user']

	tag_list=[]
	subject_list=[]

	if id and id.isdigit():
		subjects =get_subjects()

		question = get_question(int(id),u.id)
		if question:
			if request.method=='GET':
				if question['q'].tag:
					tag_list = get_c_tags(question['q'].tag)

				if question['q'].subject:
					subject_list = get_c_subjects(question['q'].subject)

				form = QuestionForm(question['q'].get_data(),auto_id='%s')
				return render_to_response(template_name,{'form':form,'tag_list':tag_list,'subject_list':subject_list,'subjects':subjects},context_instance=RequestContext(request))
		else:
			raise Http404()
	else:
		raise Http404()



def collect(request,template_name='ask/collect.html'):
	try:
		return render_to_response(template_name,context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


def add_answer(request):
	if request.is_ajax():
		u = request.session['user']
		if request.method=='POST':
			form = AnswerForm(request.POST)
			if form.is_valid():
				answer = form.save(u.id)
				if answer:
					a = get_certain_answer(answer.id)
					t = Template("""

						{% autoescape off %}
						 <div class="answer" style="border-bottom: 1px solid #ccc" >
								<a name="{{ a.answer.id }}"></a>
		                           <div class="answer_dig" >
		                              <a class="dig_up" href="javascript:void(0)" title='赞成' >
		                                  <span ></span>
		                              </a>

		                              <a class='dig_down' href="javascript:void(0)" title='反对' >
		                                  <span></span>
		                              </a>
		                          </div>
		                          <input type='hidden' value='{{ a.answer.id }}' />
		                        <h3>
		                             <a href="#">
		                                <img src="/static/image/{{ a.user.head }}" height='24' width='24'></a>
		                              <span>
		                                <a href="#">{{ a.user.nickname }}</a>
		                              </span>
		                        </h3>
		                          <div class='answer_diggers' >
		                            <span style="margin-right:10px" >{{ a.answer.agree }}赞成 / {{ a.answer.oppose }}反对</span>
	                            
	                            {% if a.dig_user %}

	                              {% for id,nickname in a.dig_user %}

	                                {% if forloop.counter <= 4 %}

	                                   {% if forloop.last %}

	                                     {% ifequal forloop.counter 4 %}
	                                          <a href="javascript:void(0)" class='expand_diggers' >更多...</a>
	                                          <span class='hide' >
	                                            <a href="#">{{ nickname }}</a>
	                                          <span>
	                                      {% else %}
	                                          <a href="#">{{ nickname }}</a>
	                                      {% endifequal %}
	                                       
	                                   {% else %}

	                                      {% ifequal forloop.counter 4 %}
	                                          <a href="javascript:void(0)" class='expand_diggers' >更多...</a>
	                                          <span class='hide' >
	                                            <a href="#">{{ nickname }}</a> 、
	                                      {% else %}
	                                          <a href="#">{{ nickname }}</a> 、
	                                      {% endifequal %}

	                                   {% endif %}           
	                                {% else %}
	                                  {% if forloop.last %}
	                                      <a href="#">{{ nickname }}</a>
	                                   </span>
	                                  {% else %}
	                                     <a href="#">{{ nickname }}</a> 、
	                                  {% endif %}
	                                  
	                                {% endif %}

	                              {% endfor %}

	                            {% endif %}
	                          </div>
		                        <div class='answer_content' style="margin-top: 5px;color:#111;line-height: 22px;" >
		                            {{ a.answer.answer }}
		                        </div>

		                        <div class="answer_action">
		                         
		                            <a href="javascript:void(0)" >评论</a>
		         
	                                <a href="javascript:void(0)" class='editanswer'  >没有帮助</a>

		                              {% ifequal a.user.id user_id %}
		                                  <a onclick='editanswer(this)' class='editanswer' href="javascript:void(0)">修改</a>
		                                  <a onclick='' class='editanswer' href="javascript:void(0)">删除</a>
		                               {%else%}

		                              {% endifequal %} 
		                              <span style='float:right;padding-top:2px' >{{ a.answer.create_time|date:'Y-m-d H:i'  }}</span> 
		                        </div>
			             </div>

			             {% endautoescape %}

					""")
					html = t.render(Context({'a':a,'user_id':u.id}))
					return HttpResponse(html)
				else:
					return HttpResponse()
			else:
				return HttpResponse()
		else:
			return HttpResponse()
	else:
		raise Http404()


def save_answer(request):
	if request.is_ajax():

		u = request.session['user']
		if request.method=='POST':
			form = AnswerForm(request.POST)
			if form.is_valid():
				answer = form.update(u.id)
				if answer:
					a = get_certain_answer(answer.id)
					t = Template("""
						{% autoescape off %}
						 <div class="answer" style="border-bottom: 1px solid #ccc" >
								  <a name="{{ a.answer.id }}"></a>
		                           <div class="answer_dig" >
		                              <a class="dig_up" href="javascript:void(0)" title='赞成' >
		                                  <span></span>
		                              </a>

		                              <a class="dig_down"  href="javascript:void(0)" title='反对' >
		                                  <span></span>
		                              </a>
		                          </div>
						         <input type='hidden' value='{{ a.answer.id }}' />
		                        <h3>
		                             <a href="#">
	                                <img src="/static/image/{{ a.user.head }}" height='24' width='24'></a>
	                              <span>
	                                <a href="#">{{ a.user.nickname }}</a>
	                              </span>
		                        </h3>
		                        <div class='answer_diggers' >
	                            <span style="margin-right:10px" >{{ a.answer.agree }}赞成 / {{ a.answer.oppose }}反对</span>
	                            
	                            {% if a.dig_user %}

	                              {% for id,nickname in a.dig_user %}

	                                {% if forloop.counter <= 4 %}

	                                   {% if forloop.last %}

	                                     {% ifequal forloop.counter 4 %}
	                                          <a href="javascript:void(0)" class='expand_diggers' >更多...</a>
	                                          <span class='hide' >
	                                            <a href="#">{{ nickname }}</a>
	                                          <span>
	                                      {% else %}
	                                          <a href="#">{{ nickname }}</a>
	                                      {% endifequal %}
	                                       
	                                   {% else %}

	                                      {% ifequal forloop.counter 4 %}
	                                          <a href="javascript:void(0)" class='expand_diggers' >更多...</a>
	                                          <span class='hide' >
	                                            <a href="#">{{ nickname }}</a> 、
	                                      {% else %}
	                                          <a href="#">{{ nickname }}</a> 、
	                                      {% endifequal %}

	                                   {% endif %}

	                                 

	                                {% else %}
	                                  {% if forloop.last %}
	                                      <a href="#">{{ nickname }}</a>
	                                   </span>
	                                  {% else %}
	                                     <a href="#">{{ nickname }}</a> 、
	                                  {% endif %}
	                                  
	                                {% endif %}

	                              {% endfor %}

	                            {% endif %}
	                          </div>
		                        <div class='answer_content' style="margin-top: 5px;color:#111;line-height: 22px;" >
		                            {{ a.answer.answer }}
		                        </div>

		                        <div class="answer_action">
		                            <a href="javascript:void(0)" >评论</a>
		                         
	                                <a href="javascript:void(0)" class='editanswer'  >没有帮助</a>

		                              {% ifequal a.user.id user_id %}
		                                  <a onclick='editanswer(this)' class='editanswer' href="javascript:void(0)">修改</a>
		                                  <a onclick='' class='editanswer' href="javascript:void(0)">删除</a>
		                               {%else%}

		                              {% endifequal %} 
		                              <span style='float:right;padding-top:2px' >{{ a.answer.create_time|date:'Y-m-d H:i'  }}</span> 
		                        </div>
			             </div>

			             {% endautoescape %}

					""")
					html = t.render(Context({'a':a,'user_id':u.id}))
					return HttpResponse(html)
				else:
					return HttpResponse()
			else:
				return HttpResponse()
		else:
			return HttpResponse()
	else:
		raise Http404()


def agree(request,id=None):
	try:
		if request.is_ajax():
			u = request.session['user']
			if id and id.isdigit():
				if post(u.id,int(id)):
					u_url = '/people/'
					if u.url:
						u_url+=u.url
					else:
						u_url+=str(u.id)

					agree_count,oppose_count=count_post(int(id))
					return HttpResponse("{status:true,url:'"+u_url+"',name:'"+u.nickname+"',agree_count:"+agree_count+",oppose_count:"+oppose_count+"}", mimetype="text/plain")
				else:
					return HttpResponse("{status:false}",mimetype="text/plain")
			else:
				return HttpResponse()
		else:
			raise Http404()
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def oppose(request,id=None):
	try:
		if request.is_ajax():

			u = request.session['user']
			if id and id.isdigit():
				if post(u.id,int(id),action='oppose'):
					u_url = '/people/'
					if u.url:
						u_url+=u.url
					else:
						u_url+=str(u.id)
					agree_count,oppose_count=count_post(int(id))
					return HttpResponse("{status:true,url:'"+u_url+"',name:'"+u.nickname+"',agree_count:"+agree_count+",oppose_count:"+oppose_count+"}", mimetype="text/plain")
				else:
					return HttpResponse("{status:false}",mimetype="text/plain")
			else:
				return HttpResponse()
		else:
			raise Http404()
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass