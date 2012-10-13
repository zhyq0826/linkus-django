# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.views.csrf import csrf_failure

from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

from auth.views import login
from public.views import reading


def csrf_failure(request,reason=""):
	return redirect('/accounts/login')

def index(request,template_name='index.html'):
	try:
		u = request.session['user']
		if u:
			return redirect('/read/')
		else:
			return login(request,template_name)
	except KeyError:
		#未登录则重定向到登陆首页
		return login(request,template_name)


def not_found(request,template_name='404.html'):
	try:
		return render_to_response(template_name)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass