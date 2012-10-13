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

blog_template_prefix='blog/'


def view_blog(request,template_name=blog_template_prefix+'blog_view.html',id=None):
	try:

		s = request.GET.get('subject')
		people = request.GET.get('people')

		tags=[]
		subjects=[]
	
		if id and id.isdigit():
			id = int(id)
			article =  get_article(int(id))
			
			if not article:
				raise Http404()

			author = get_author(article.user_id)

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
			if s and s.isdigit():
				one = get_one_subject(int(s))
				if one:
					next_article = get_subject_next_article(int(s),id)
					prev_article = get_subject_prev_article(int(s),id)
				else:
					raise Http404()	
			else:
				next_article = get_next_article(id)
				prev_article = get_prev_article(id)
				one=None

			data={'article':article,'one':one,'comment_count':comment_count,'author':author,'tags':tags,'subjects':subjects,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size,'comments':comments,'next_article':next_article,'prev_article':prev_article}
			return render_to_response(template_name,data,context_instance=RequestContext(request))
		else:
			raise Http404()
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass



def write_blog(request,template_name=blog_template_prefix+'blog_write.html'):
	try:
		u = request.session['user']

		subjects = get_subjects()

			
		
		if request.method=='GET':
			form = ArticleForm(user_id=u.id,auto_id='%s')
			return render_to_response(template_name,{'form':form,'subjects':subjects},context_instance=RequestContext(request))
		else:
			tag_list = request.POST.getlist('tag_list')
			subject_list = request.POST.getlist('subject_list')
			#这里参数关键字的问题
			form = ArticleForm(request.POST,user_id=u.id,auto_id='%s')
			if form.is_valid():
				form.save(u.id,tag_list,subject_list)
				if u.url:
					return redirect('/people/'+u.url+'/blog')
				else:
					use_id = str(u.id)
					return redirect('/people/'+use_id+'/blog')
			else:
				return render_to_response(template_name,{'form':form,'subjects':subjects},context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass


def edit_blog(request,template_name=blog_template_prefix+'blog_edit.html',id=None):
	try:
		u = request.session['user']


		
		if id and id.isdigit():
			article = get_article(id,u.id)

			subjects = get_subjects()

			tag_list=[]
			subject_list=[]

			
			
			if article:
				if article.tag:
					tag_list = get_c_tags(article.tag)

				if article.subject:
					subject_list = get_c_subjects(article.subject)
					
				form = ArticleForm(user_id=u.id,initial=article.get_data(),auto_id='%s')
				time=article.create_time
				return render_to_response(template_name,{'form':form,'time':time,'subjects':subjects,'tag_list':tag_list,'subject_list':subject_list},context_instance=RequestContext(request))
			else:
				raise Http404()
		else:
			raise Http404()
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def save_blog(request,template_name=blog_template_prefix+'blog_edit.html'):
	try:
		u = request.session['user']
		
		if request.method=='POST':
			
			tag_list = request.POST.getlist('tag_list')
			subject_list = request.POST.getlist('subject_list')

			form = ArticleForm(request.POST,user_id=u.id,auto_id='%s')
			if form.is_valid():
				form.update(u.id,tag_list,subject_list)
				if u.url:
					return redirect('/people/'+u.url+'/blog')
				else:
					id = str(u.id)
					return redirect('/people/'+id+'/blog')
			else:
				return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

#根据普通请求请求文章和页面
# def getarticles(request,id=None):
# 	try:
# 		u = request.session['user']
# 		if id and id.isdigit():

# 			page_number = request.GET.get('page')
# 			paginator = Paginator(get_article_total_count(u.id,int(id)),20)

# 			if page_number and page_number.isdigit():
# 				try:
# 					page = paginator.page(int(page_number))
# 					pages = paginator.calculate_display_pages(int(page_number))
# 				except EmptyPage:
# 					page = paginator.page(1)
# 					pages = paginator.calculate_display_pages(1)
# 			else:
# 				page = paginator.page(1)
# 				pages = paginator.calculate_display_pages(1)
			
# 			articles = get_limit_articles(u.id,page.start,page.end,catalog_id=int(id))
						
# 			less_than_certain_size = paginator.check_less_than_certain_size()
			
# 			t = Template("""

# 					{% autoescape on %} 
# 					<ul>
# 					{% for article in articles %}
# 					<li> 
# 						<div class="title" ><a href="/blog/{{ article.id}}?catalog={{catalog_id}}" >{{ article.title }}</a></div>
# 						<div class="edit" >
# 							<span class="edit_time" >{{ article.create_time|date:"Y-m-d H:i" }}</span> 
# 							<span class="edit_action" >
# 							<a href="/blog/edit/{{article.id }}" >编辑</a>
# 							<a href="#" >评论</a>
# 							<a href="#" >更多</a>
# 						</span> 
# 						</div
# 					</li>
# 					{% endfor %}
# 					</ul>
# 				    <div class="page" >

#                     {% if page.prev_page_number and not less_than_certain_size %}
#                        <a href="{{ user_url }}/blog?page={{ page.prev_page_number }}&catalog={{ catalog_id }}" class="prev"> <<-上一页</a>
#                     {% endif %}

#                     {% for key,value in pages %}


#                         {% ifequal page.page_number key %}

#                             <a href="{{ user_url }}/blog?page={{ key }}&catalog={{ catalog_id }}" class="current_page" >  {{ value.page_number }}  </a>

#                         {% else %}

#                                 <a href="{{ user_url }}/blog?page={{ key }}&catalog={{ catalog_id }}" >  {{ value.page_number }}  </a>

#                         {% endifequal %}

#                     {% endfor %}
                    
#                     {% if page.has_next  and not less_than_certain_size %}
#                          <a href="{{ user_url }}/blog?page={{ page.next_page_number }}&catalog={{ catalog_id }}" class="next" >下一页->></a>
#                     {% endif %}
                    
#                     </div>
# 					{% endautoescape %}
# 				"""
# 			)
# 			data={'articles':articles,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size,'catalog_id':id}
# 			html = t.render(Context(data))
# 			return HttpResponse(html)
# 		else:
# 			return HttpResponse()
# 	except Exception, e:
# 		raise
# 	else:
# 		pass
# 	finally:
# 		pass

#根据ajax请求文章和分页
# def getarticles(request,id=None):
# 	try:
# 		u = request.session['user']
# 		if u:
# 			if id and id.isdigit():
# 				articles = get_articles_by_catalog(int(id))
# 				page_number = request.GET.get('page')
# 				paginator = Paginator(get_article_total_count(u.id,int(id)),10)

# 				if page_number and page_number.isdigit():
# 					try:
# 						page = paginator.page(int(page_number))
# 						pages = paginator.calculate_display_pages(int(page_number))
# 					except EmptyPage:
# 						page = paginator.page(1)
# 						pages = paginator.calculate_display_pages(1)
# 				else:
# 					page = paginator.page(1)
# 					pages = paginator.calculate_display_pages(1)
				
# 				articles = get_limit_articles(u.id,page.start,page.end,catalog_id=int(id))
# 				less_than_certain_size = paginator.check_less_than_certain_size()
				
# 				t = Template("""

# 						{% autoescape on %} 
# 						<ul>
# 						{% for article in articles %}
# 						<li> 
# 							<div class="title" ><a href="{% url blog.iviews.view_blog article.id %}?catalog={{catalog_id}}" >{{ article.title }}</a></div>
# 							<div class="edit" > \
# 								<span class="edit_time" >{{ article.create_time|date:"Y-m-d H:i" }}</span> 
# 								<span class="edit_action" >
# 								<a href="{% url blog.iviews.edit_blog article.id %}" >编辑</a>
# 								<a href="#" >评论</a>
# 								<a href="#" >更多</a>
# 							</span> 
# 							</div
# 						</li>
# 						{% endfor %}
# 						</ul>
# 						    <div class="page" >

#                        {% if page.prev_page_number and not less_than_certain_size %}
#                            <a onclick='get_articles_by_page({{catalog_id}},{{ page.prev_page_number }})' href="#" class="prev"> <<-上一页</a>
#                        {% endif %}
#                          {% for key,value in pages %}

#                             {% ifequal page.page_number key %}

#                                 <a onclick='get_articles_by_page({{catalog_id}},{{ key }})' href="#" style='background-color:#d21a00;color:#fff;border-color:#fff' >  {{ value.page_number }}  </a>

#                             {% else %}

#                                     <a onclick='get_articles_by_page({{catalog_id}},{{ key }})' href="#" >  {{ value.page_number }}  </a>

#                             {% endifequal %}

#                          {% endfor %}
                        
#                          {% if page.has_next  and not less_than_certain_size %}
#                              <a onclick='get_articles_by_page({{catalog_id}},{{ page.next_page_number }})' href="#" class="next" >下一页->></a>
#                          {% endif %}

#                           </div>
# 						{% endautoescape %}
# 					"""
# 				)
# 				data={'articles':articles,'page':page,'pages':pages,'less_than_certain_size':less_than_certain_size,'catalog_id':id}
# 				html = t.render(Context(data))
# 				return HttpResponse(html)
# 	except Exception, e:
# 		raise
# 	else:
# 		pass
# 	finally:
# 		pass

#只请求文章根据ajax
# def getarticles(request,id=None):
# 	try:
# 		u = request.session['user']
# 		if u:
# 			if id and id.isdigit():
# 				articles = get_articles_by_catalog(int(id))
# 				t = Template("""
# 						{% autoescape on %} 
# 						{% for article in articles %}
# 						<li> 
# 							<div class="title" ><a href="{% url blog.iviews.view_blog article.id %}?catalog={{catalog_id}}" >{{ article.title }}</a></div>
# 							<div class="edit" > \
# 								<span class="edit_time" >{{ article.create_time|date:"Y-m-d H:i" }}</span> 
# 								<span class="edit_action" >
# 								<a href="{% url blog.iviews.edit_blog article.id %}" >编辑</a>
# 								<a href="#" >评论</a>
# 								<a href="#" >更多</a>
# 							</span> 
# 							</div
# 						</li>
# 						{% endfor %}
# 						{% endautoescape %}
# 					"""
# 				)
# 				html = t.render(Context({'articles':articles,'catalog_id':id}))
# 				return HttpResponse(html)
# 	except Exception, e:
# 		raise
# 	else:
# 		pass
# 	finally:
# 		pass



def comment_blog(request):
	try:
		u = request.session['user']
		form = ArticleCommentForm(request.POST)
		if form.is_valid():
			comment = form.save(u.id)
			comment = get_atcile_comment(comment.id)
			if comment:
				# reponse_data = """{
				#         status:true,
				#         comment:{
				# 			content:'{{ c.comment.content }}',
				# 			to_user_id:'{{ c.comment.to_user_id }}',
				# 			to_nickname:'{{ c.to_user.nickname }}',
				# 			user_id:'{{ c.user.id }}',
				# 			nickname:'{{ c.user.nickname }}',
				# 			create_time:'{{ c.comment.create_time|date:'Y-m-d H:i'}}'
				# 		}
				# 	}
				# """
				# replace_blank = lambda x:''.join(x.split(' '))
				reponse_data="""
				<li>
                    <a class="head" >
                        <img src="/img/avatar/yj1.jpg"  />
                    </a>
                    {% if c.to_user %}
                        <label>RT <a href="javascript:void(0)">{{ c.to_user.nickname }}:</a></label>
                    {% endif %}
                    <table  style="table-layout:fixed" width="600" >
                        <tbody>
                                <td style="word-wrap : break-word; overflow:hidden; " >
                               <prev>
			                        {{ c.comment.content }}
			                    </prev>
                              </td>
                              </tbody>
                    </table>
                    <div>
                        <span class="comment_time" > {{ c.comment.create_time|date:'Y-m-d H:i'}}</span>
                        <span class="comment_user" >
                            <a href="#" class="replied" >{{ c.user.nickname }}</a>
                            <a  href="javascript:void(0)" class="reply" ></a>
                            <input type="hidden"  value="{{ c.user.id }}" />
                        </span>
                    </div>
                  </li>

				"""
				t = Template(reponse_data)
				html = t.render(Context({"c":comment}))
				return HttpResponse(html)
			else:
				return HttpResponse()
		else:
			return HttpResponse()
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass