#-*- coding:utf-8 -*-
from django.http import HttpResponse,Http404
from django.template import Template,Context,RequestContext,TemplateDoesNotExist
from django.shortcuts import render_to_response,redirect
from forms import *
from linkusall.util import Paginator,EmptyPage
from linkusall.subject.models import get_subjects,get_c_tags,get_c_subjects

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

topic_template_prefix='topic/'



def loadcomment(request,id=None):
	try:
		if id and id.isdigit():
			comments = get_limit_topic_comments(int(id),0,10)
			total = get_topic_comments_count(int(id))
			morecomment = 0

			t=Template("""
			  <div class="comment" >
                <ul>
                    <div class='loadingchange' >
                            <img src="/static/image/ajax-loader.gif" width='22' height='22' >
                            <span>
                                正在加载,请稍后...
                            </span>
                    </div>
		            <form name='commentform{{ topic_id }}' >
		                <li style="border:none;padding:0px"  >
		                    <textarea name='content' ></textarea>
		                    <input type="hidden" name="to_user_id" value='' />
			                <input type="hidden" name="topic_id" value="{{ topic_id }}" >
		                </li>
		                <input type="button" onclick="submitComment('commentform{{ topic_id }}')" class="action"  value="回应" />
			            <div style='height:15px;clear:borth' ></div>
		            </form>
		           
		            {% for c in comments %}
		                <li  >
		                   <a class="head" >
		                        <img src="/img/avatar/{{ c.user.head }}" />
		                    </a>


		                    {% if c.to_user %}
		                        <label>RT <a href="javascript:void(0)">{{ c.to_user.nickname }}:</a></label>
		                    {% endif %}


		                    <table  style="table-layout:fixed" width="634" >
		                        <tbody>
                                <td style="word-wrap : break-word; overflow:hidden; " >
                               <prev>
			                        {{ c.content }}
			                    </prev>
                              </td>
                              </tbody>
		                    </table>
		                    <div>
		                        <span class="comment_time" >{{ c.create_time|date:'Y-m-d H:i' }}</span>
		                        <span class="comment_user" >
		                            <a href="#" class="replied" >{{ c.user.nickname }}</a>
		                            <a  href   ="javascript:void(0)" class="reply" ></a>
		                            <input type="hidden" name="user_id"  value="{{ c.user.id }}" />
                                    <input type="hidden" name="id"  value="commentform{{ topic_id }}" />
		                        </span>
		                    </div>
		                </li>
		            {% endfor %}
		            {% if morecomment %}
		                <span class='morecomment' >还有{{ morecomment }}条回应,<a  href="/topic/{{ topic_id }}">点击查看</a></span>
		            {% endif %}
		        </ul>

		        </div>
			""")
			if total>10:
				morecomment=total-10
			html = t.render(Context({'comments':comments,'morecomment':morecomment,'topic_id':id}))
			return HttpResponse(html)
		else:
			return HttpResponse()
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


def comment_topic(request):
	try:
		u = request.session['user']
		form = TopicCommentForm(request.POST)
		if form.is_valid():
			c = form.save(u.id)
			comments = get_certain_one_topic_comment(c.id)
			t=Template("""
				 <li>

	                   <a class="head" >
	                        <img src="/img/avatar/{{ c.user.head }}" />
	                    </a>
	                    

	                    {% if c.to_user %}
	                        <label>RT <a href="javascript:void(0)">{{ c.to_user.nickname }}:</a></label>
	                    {% endif %}


	                     <table  style="table-layout:fixed">
		                        <tbody>
		                        <td style="word-wrap : break-word; overflow:hidden; " >
		                       <prev>
		                            {{ c.content }}
		                        </prev>
		                      </td>
		                      </tbody>
	                    </table>
	                    <div>
	                        <span class="comment_time" >{{ c.create_time|date:'Y-m-d H:i' }}</span>
	                        <span class="comment_user" >
	                            <a href="#" class="replied" >{{ c.user.nickname }}</a>
	                            <a  href="javascript:void(0)" class="reply" ></a>
	                            <input type="hidden" name="user_id"  value="{{ c.user.id }}" />
	                            <input type="hidden" name="id"  value="commentform{{ c.topic_id }}" />
	                        </span>
	                    </div>
	                </li>
				""")
			html = t.render(Context({'c':comments[0]}))
			return HttpResponse(html)
		else:
			return HttpResponse()
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass



def new_topic(request,template_name=topic_template_prefix+'topic_new.html'):
	try:
		u = request.session['user']
		
		subjects = get_subjects()

		if request.method=='GET':
			form = TopicForm(auto_id='%s')
			return render_to_response(template_name,{'form':form,'subjects':subjects},context_instance=RequestContext(request))
		else:
			
			tag_list=[]
			subject_list=[]

			tag_list = request.POST.getlist('tag_list')
			subject_list = request.POST.getlist('subject_list')

			form = TopicForm(request.POST)
			if form.is_valid():
				form.save(u.id,tag_list,subject_list)

				return redirect('/topic')
			else:
				return render_to_response(template_name,{'form':form,'subjects':subjects},context_instance=RequestContext(request))
	except Exception,e:
		raise 
	else:
		pass
	finally:
		pass


def topic_detail(request,template_name=topic_template_prefix+'topic_detail.html',id=None):
	try:
		u = request.session['user']
		if id and id.isdigit():
			topic = get_certain_one_topoc(int(id))

			tags=[]
			subjects=[]

			if topic['tag']:
				tags = get_c_tags(topic['tag'])

			if topic['subject']:
				subjects = get_c_subjects(topic['subject'])

			#开始对评论分页
			paginator = Paginator(topic['comment_count'],20)
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
			comments = get_limit_topic_comments(int(id),page.start,page.end)
			data={'comments':comments,'topic_id':topic['id'],'tags':tags,'subjects':subjects,'t':topic,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size}
			return render_to_response(template_name,data,context_instance=RequestContext(request))
		else:
			raise Http404()
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def topic(request,template_name='public/topic.html'):
	try:
		u = request.session['user']


		total_count = get_topic_total_count()

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
		topics = get_limit_topics(start=page.start,end=page.end)
		data={'topics':topics,'all_current':'ana_focus_current','total_count':total_count,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size}
		return render_to_response(template_name,data,context_instance=RequestContext(request))
	except Exception, e:
		raise 
	else:
		pass
	finally:
		pass

	