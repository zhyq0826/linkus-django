#-*- coding:utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from linkusall.auth.models import User
from linkusall.util import custom_raw_sql as execute_sql

def check_user_follow(user_id,follow_id):
	sql = "select * from follow where user_id=%d and follow_id=%d and type=1 "%(user_id,follow_id)
	result = execute_sql(sql)
	if result:
		return True
	else:
		return False

def get_user_following(user_id):
	
	sql = "select user_id from follow as f where f.follow_id=%d and type=1"%(user_id)

	result = execute_sql(sql)
	data=[]
	try:
		for user_id in result:
			id=user_id[0]
			user = User.objects.get(id=id)
			data.append(user)
		return data
	except Exception, e:
		return None

def get_user_follower(user_id):
	sql = "select follow_id from follow as f where f.user_id=%d and type=1"%(user_id)

	result = execute_sql(sql)
	data=[]
	try:
		for follow_id in result:
			id=follow_id[0]
			user = User.objects.get(id=id)
			data.append(user)
		return data
	except Exception, e:
		return None

	

