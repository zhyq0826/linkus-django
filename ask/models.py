#-*- coding:utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.core.mail import send_mail
from datetime import datetime
from linkusall.auth.models import User
from linkusall.util import custom_raw_sql as execute_sql
from linkusall.util import execute_subject_query
from linkusall.subject.models import get_subjects,get_c_subjects,get_c_tags
from linkusall.setting.models import UserSchool

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

class Question(models.Model):
	user_id = models.IntegerField(max_length=11)
	question = models.TextField()
	question_more=models.TextField()
	create_time = models.DateTimeField()
	comment_count = models.IntegerField(max_length=11,default=0)
	answer_count = models.IntegerField(max_length=11,default=0)
	anonymity = models.IntegerField(max_length=1,default=0)
	subject = models.CharField(max_length=250)
	tag = models.CharField(max_length=250)
	close_state = models.IntegerField(max_length=1,default=0)
	last_update_time = models.DateTimeField()

	class Meta:
		db_table='question'
		ordering=['-create_time']

	def get_data(self):
		return{
		'question':self.question,
		'more':self.question_more,
		'id':self.id,
		'anonymity':self.anonymity
		}


class QuestionComment(models.Model):
	q_id= models.IntegerField(max_length=11)
	user_id = models.IntegerField(max_length=11)
	content=models.TextField()
	create_time = models.DateTimeField()

	class Meta:
		db_table='question_comment'


class Answer(models.Model):
	q_id = models.IntegerField(max_length=11)
	user_id = models.IntegerField(max_length=11)
	answer = models.TextField()
	create_time = models.DateTimeField()
	comment_count = models.IntegerField(max_length=11,default=0)
	agree = models.IntegerField(max_length=11,default=0)
	oppose = models.IntegerField(max_length=11,default=0)

	class Meta:
		db_table='answer'
		ordering=['create_time']

class AnswerComment(models.Model):
	a_id= models.IntegerField(max_length=11)
	user_id = models.IntegerField(max_length=11)
	content=models.TextField()
	create_time = models.DateTimeField()

	class Meta:
		db_table='answer_comment'

class UserAskAnswerState(models.Model):
	id = models.IntegerField(primary_key=True,max_length=11)
	question_count=models.IntegerField(max_length=11,default=0)
	answer_count=models.IntegerField(max_length=11,default=0)
	asking_count=models.IntegerField(max_length=11,default=0)
	thanks_count=models.IntegerField(max_length=11,default=0)
	useful_count=models.IntegerField(max_length=11,default=0)
	create_time=models.DateTimeField()

	class Meta:
		db_table='user_ask_answer_state'

class AnswerDig(models.Model):
	a_id = models.IntegerField(primary_key=True,max_length=11)
	user_id = models.IntegerField(primary_key=True,max_length=11)
	dig_status=models.IntegerField(max_length=11,default=0)

	class Meta:
		db_table='answer_dig'

def get_questions_by_subject(id,start=None,end=None):
	data=[]
	sql = "select id,user_id,question,answer_count,create_time,subject,tag,anonymity from question  where subject like %s or subject like %s limit "+str(start)+","+str(end)+""
	questions=execute_subject_query(id,sql=sql)
	for a in questions:
		q_id,user_id,question,answer_count,create_time,subject,tag,anonymity=a
		q={}
		q['id']=q_id
		q['user_id']=user_id
		q['question']=question
		q['answer_count']=answer_count
		q['create_time']=create_time
		q['anonymity']=anonymity
		one = {}
		one['q']=q
		one['u']=User.objects.get(id=user_id)
		one['s']=get_c_subjects(subject)
		one['t']=get_c_tags(tag)
		data.append(one)

	return data

#某个主题的问题总量
def get_some_subject_question_count(id):
	return execute_subject_query(id,'question')[0][0]

def get_user_ask_answer_state(user_id):
	try:
		return UserAskAnswerState.objects.get(id=user_id)
	except ObjectDoesNotExist:
		return None
	else:
		pass
	finally:
		pass

#检查用户是否提交了答案
def check_user_answer_state(q_id,user_id):
	user_answer = Answer.objects.filter(q_id=q_id,user_id=user_id)
	if user_answer:
		return user_answer[0]

	return user_answer

#查询某一个问题
def get_question(id,user_id=None):
	if user_id:
		q = Question.objects.filter(id=id,user_id=user_id)
	else:
		q = Question.objects.filter(id=id)
	data={}
	if q:
		data['q']=q[0]
		try:
			#匿名问题不提取用户名
			if q[0].user_id:
				data['user']=User.objects.filter(id=q[0].user_id).values('id','nickname','role','head','url')[0]
		except IndexError, e:
			pass

	return data

def get_answer(id):
	a = Answer.objects.filter(id=id)
	data={}
	if a:
		data['a']=a[0]
		try:
			if a[0].user_id:
				data['user']=User.objects.filter(id=a[0].user_id).values('id','nickname','role','head')[0]
		except IndexError, e:
			pass

	return data

def count_post(id):
	sql = "select count(*) from answer_dig a where a.a_id=%d and dig_status=1 "%(id)
	agree_count = execute_sql(sql)
	agree_count=agree_count[0][0]


	sql = "select count(*) from answer_dig a where a.a_id=%d and dig_status=-1 "%(id)
	oppose_count = execute_sql(sql)
	oppose_count=oppose_count[0][0]

	return str(agree_count),str(oppose_count)


def get_certain_answer(id):
	answers = Answer.objects.filter(id=id)
	data={}
	if answers:
		try:
			one={}
			sql = "select dig_status from answer_dig a where a.a_id=%d and a.user_id=%d"%(answers[0].id,answers[0].user_id)
			dig_data=execute_sql(sql)
			if dig_data:
				one['dig_status']=dig_data[0][0]

			sql = "select count(*) from answer_dig a where a.a_id=%d and dig_status=1 "%(answers[0].id)
			agree_count = execute_sql(sql)
			one['agree_count']=agree_count[0][0]


			sql = "select count(*) from answer_dig a where a.a_id=%d and dig_status=-1 "%(answers[0].id)
			oppose_count = execute_sql(sql)
			one['oppose_count']=oppose_count[0][0]



			sql = "select u.id,u.nickname,IFNULL(u.url,u.id),u.role from answer_dig a,user u where a.a_id=%d and dig_status=1 and a.user_id=u.id "%(answers[0].id)	
			dig_user = execute_sql(sql)

			if dig_user:
				one['dig_user']=dig_user
			one['answer']=answers[0]
			one['user'] = User.objects.filter(id=answers[0].user_id).values('id','nickname','role','head','url')[0]
			data = one
		except IndexError, e:
			pass


	return data		


#获取指定数量的答案
def get_limit_answers(q_id,start=0,end=0):
	answers = Answer.objects.filter(q_id=q_id)[start:end]
	data=[]
	if answers:
		for i in range(0,answers.count()):
			try:
				one={}
				sql = "select dig_status from answer_dig a where a.a_id=%d and a.user_id=%d"%(answers[i].id,answers[i].user_id)
				dig_data=execute_sql(sql)
				if dig_data:
					one['dig_status']=dig_data[0][0]

				sql = "select count(*) from answer_dig a where a.a_id=%d and dig_status=1 "%(answers[0].id)
				agree_count = execute_sql(sql)
				one['agree_count']=agree_count[0][0]


				sql = "select count(*) from answer_dig a where a.a_id=%d and dig_status=-1 "%(answers[0].id)
				oppose_count = execute_sql(sql)
				one['oppose_count']=oppose_count[0][0]

				sql = "select u.id,u.nickname,IFNULL(u.url,u.id),u.role from answer_dig a,user u where a.a_id=%d and dig_status=1 and a.user_id=u.id "%(answers[i].id)	
				dig_user = execute_sql(sql)
				if dig_user:
					one['dig_user']=dig_user
				one['answer']=answers[i]
				one['user'] = User.objects.filter(id=answers[i].user_id).values('id','nickname','role','head','url')[0]
				data.append(one)		
			except IndexError:
				pass

	return data


def get_question_answer_count(q_id):
	return Answer.objects.filter(q_id=q_id).count()


def get_question_total_count(user_id=None):
	if not user_id:
		return Question.objects.filter().count()
	return Question.objects.filter(user_id=user_id).count()

#按时间排序取得问题
def get_limit_questions(user_id=None,start=None,end=None,order=None,filter=None):

	if start>=0 and end>=start:
		if not user_id:
			data=[]
			if not order:
				questions= Question.objects.filter().order_by('-last_update_time','-create_time')[start:end]
			else:
				questions = Question.objects.filter().order_by(order,'-create_time')[start:end]

			if questions:
				for q in questions:
					one = {}
					one['q']=q
					one['u']=User.objects.get(id=q.user_id)
					one['s']=get_c_subjects(q.subject)
					one['t']=get_c_tags(q.tag)
					data.append(one)
			
			return data


		questions = Question.objects.filter(user_id=user_id)[start:end]

	else:
		questions = Question.objects.filter(user_id=user_id)

	return questions

#按时间排序取得问题
def get_limit_anonymity_questions(user_id=None,start=None,end=None,order='-answer_count'):

	if start>=0 and end>=start:
		if not user_id:
			data=[]
			questions = Question.objects.filter(anonymity=1).order_by(order,'-create_time')[start:end]
			if questions:
				for q in questions:
					one = {}
					one['q']=q
					one['s']=get_c_subjects(q.subject)
					one['t']=get_c_tags(q.tag)
					data.append(one)
			return data

		questions = Question.objects.filter(user_id=user_id)[start:end]

	else:
		questions = Question.objects.filter(user_id=user_id)

	return questions


#用户回答过的问题,包括匿名问题和非匿名问题
def get_limit_answered_questions(user_id,start=None,end=None):
	if start>=0 and end>=start:
		sql = """
		select q.id,q.user_id,q.question,a.id,a.answer,a.create_time 
		from answer as a ,question as q 
		where a.user_id=%d and a.q_id=q.id 
		ORDER BY a.create_time desc limit %d,%d
		""" % (user_id,start,end)
		answered_questions = execute_sql(sql)

	return answered_questions


def post(user_id,a_id,action='agree'):
	try:
		a = Answer.objects.get(id=a_id)
		if action=='agree':
			if AnswerDig.objects.filter(user_id=user_id,a_id=a_id):
				sql = "update answer_dig a set a.dig_status=1 where a.a_id=%d and a.user_id=%d"%(a_id,user_id)
				execute_sql(sql,operation='update')
			else:
				sql = "insert into answer_dig(a_id,user_id,dig_status)values(%d,%d,%d)"%(a_id,user_id,1)
				execute_sql(sql,operation='insert')

		else:
			if AnswerDig.objects.filter(user_id=user_id,a_id=a_id):
				sql = "update answer_dig a set a.dig_status=-1 where a.a_id=%d and a.user_id=%d"%(a_id,user_id)
				execute_sql(sql,operation='update')
			else:
				sql = "insert into answer_dig(a_id,user_id,dig_status)values(%d,%d,%d)"%(a_id,user_id,-1)
				execute_sql(sql,operation='insert')

		return True
	except Exception, e:
		return False
	else:
		pass
	finally:
		pass

def close(user_id,q_id,action='close'):
	try:
		if action=='close':
			status = Question.objects.filter(user_id=user_id,id=q_id).update(close_state=1)
		else:
			status = Question.objects.filter(user_id=user_id,id=q_id).update(close_state=0)
		if status:
			return True
		else:
			return False
	except Exception, e:
		return False
	
	


#因为字典是无序的，先进行排序
def sort_dict_values(adict):
	if adict:	
		keys = adict.keys()
		keys.sort()
		return [(key,adict[key]) for key in keys]

	return adict


def get_i_college_question_count(user_id):
	us = UserSchool.objects.get(id=user_id)
	if us.college:
		sql=" select count(*) from user_school as us,question as a where us.college = "+str(us.college)+" and a.user_id = us.id"
		result = execute_sql(sql)
		if result:
			return result[0][0]
		else:
			return 0


def get_i_college_limit_questions(user_id,start,end):
	us = UserSchool.objects.get(id=user_id)
	data=[]
	if us.college:
		sql = "select a.id,a.user_id,a.question,a.create_time,a.answer_count,a.tag,a.subject from user_school us,question a where us.college="+str(us.college)+" and us.id = a.user_id order by create_time desc,answer_count desc limit "+str(start)+","+str(end)+""
		results=execute_sql(sql)
		for a in results:
			id,user_id,question,create_time,answer_count,tag,subject=a
			q={}
			q['id']=id
			q['user_id']=user_id
			q['topic']=question
			q['comment_count']=answer_count
			q['create_time']=create_time
			q['question']=question
			one={}
			one['s']=get_c_subjects(subject)
			one['t']=get_c_tags(tag)
			one['q']=q
			one['u']=User.objects.get(id=user_id)
			data.append(one)

	return data

