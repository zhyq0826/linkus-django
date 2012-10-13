# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext,Template, Context
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
from models import *
import re

from django.http import Http404,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError

from linkusall.util import custom_raw_sql as execute_sql



def yesfollow(request,id=None):
	u = request.session['user']
	if id and id.isdigit():
		id = int(id)
		sql = "select * from follow where user_id=%d and follow_id=%d"%(id,u.id)
		result = execute_sql(sql)
		if result:
			sql = "update follow f set f.type = 1 where user_id=%d and follow_id=%d" %(id,u.id)
			execute_sql(sql,operation="update")
		else:
			sql = "insert into follow values(%d,%d,1)" %(id,u.id)
			execute_sql(sql,operation="insert")

		return HttpResponse()
	else:
		raise Http404()

def nofollow(request,id=None):
	u = request.session['user']
	if id and id.isdigit():
		id = int(id)
		sql = "select * from follow where user_id=%d and follow_id=%d"%(id,u.id)
		result = execute_sql(sql)
		if result:
			sql = "update follow f set f.type = 0 where user_id=%d and follow_id=%d" %(id,u.id)
			execute_sql(sql,operation="update")
		else:
			sql = "insert into follow values(%d,%d,0)" %(id,u.id)
			execute_sql(sql,operation="insert")
		return HttpResponse()
	else:
		raise Http404()


def follow(request,template_name="follow/i/follow.html"):
	u = request.session['current_user']
	login_u = request.session['user']
	following=None
	follower=None
	if u.id == login_u.id:
		pass
	else:
		template_name="follow/follow.html"
		following = follow = get_user_following(u.id)
		follower = get_user_follower(u.id)

	follow = get_user_following(u.id)
	return render_to_response(template_name,{'follow':follow,'following':following,'follower':follower},context_instance=RequestContext(request))


def follower(request,template_name="follow/i/follow.html"):
	u = request.session['current_user']

	login_u = request.session['user']
	if u.id == login_u.id:
		pass
	else:
		template_name="follow/follow.html"

	follow = get_user_follower(u.id)
	return render_to_response(template_name,{'follow':follow},context_instance=RequestContext(request))