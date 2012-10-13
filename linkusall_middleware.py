#-*-coding:utf-8-*-
from django.http import HttpResponseRedirect,HttpResponsePermanentRedirect 
from django.template import Template,Context
from django.template.loader import get_template
from django.http import Http404,HttpResponse
from django.contrib.auth import SESSION_KEY    
from urllib import quote
from django.shortcuts import render_to_response,redirect
from auth.forms import LoginForm    
import re
from auth.models import User,get_user

class LoginAuthMiddleware(object):
	#对于每个请求，检测其user，存在不处理,存在但为空，进入登陆页面,不存在，如果是首页和登陆页，直接进入，否则进入登陆页
	def process_request(self,request):
		try:
			re_people =  re.compile(r"/people/([a-zA-Z0-9]{1,20})")
			if not request.path.startswith('/img/') and not request.path.startswith('/static/'):
				u = request.session['user']
				if u:
					#如果请求的是首页和登陆页如果用户已经登陆导向主页
					if request.path=='/':
						pass
					if request.path=='/accounts/login/':
						return redirect('/')
						

					#如果请求的是用户主页,提取用户url或者id
					if request.path.startswith('/people/'):
						m = re_people.search(request.path)
						id = ''
						if m:
							try:
								id = m.group(1)
							except Exception, e:
								raise Http404()
						else:
							raise Http404()

						current_user = request.session['current_user']
						#检测当前访问的用户是否是current_user,如果不是取得用户信息,如果没有用户，抛出404
						if current_user:
							if current_user.id ==id or current_user.url==id:
								request.session['current_user']=u
							else:
								current_user = get_user(id)
								if current_user:
									request.session['current_user']=current_user
								else:
									raise Http404()
						
					else:
						pass
				else:
					
					#如果请求时要求登陆，则不做处理
					if request.path=='/accounts/login/' or request.path=='/' or request.path.startswith('/accounts/'):
						pass
					else:
						#特别处理ajax请求
						if request.is_ajax():
							return HttpResponse()

						return redirect('/accounts/login/')
		except KeyError:
			request.session['user']=None
			if request.path=='/accounts/login/' or request.path=='/' or request.path.startswith('/accounts/'):
				pass
			else:

				if request.is_ajax():
						return HttpResponse()

				return redirect('/accounts/login/')

    #处理登陆后的处理，如果返回的是keyerro说明cookie禁用了,进入登陆页,如果不是，则返回正常的响应
	def process_response(self,request,repsonse):
		# if repsonse.content.strip()=='KeyError':
		# 	return self.__login_response()
		# else:
		return repsonse


	def __login_response(self):
		form = LoginForm(auto_id='%s')
		return render_to_response('auth/login.html',{'form':form})


	def __test_reponse(self):
		return HttpResponse("test", mimetype="text/plain")
	

	

