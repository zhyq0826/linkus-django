# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext,Template, Context
from auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
from forms import *
from models import *



from django.http import Http404,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 



#使用上下文context
def home(request,template_name='home/home.html',id=None):
	try:
		u = request.session['user']
		if u:
			return render_to_response(template_name,context_instance=RequestContext(request))
		else:
			return redirect('/accounts/login/')
	except KeyError:
		#没有登录重定向到首页
		return redirect('/accounts/login/')
	else:
		pass
	finally:
		pass
	

