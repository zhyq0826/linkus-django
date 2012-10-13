#-*- coding:utf-8 -*-
from django.db import models
from linkusall.auth.models import User
from linkusall.util import execute_subject_query,custom_raw_sql
from linkusall.subject.models import get_subjects,get_c_subjects,get_c_tags
from linkusall.setting.models import UserSchool


class Topic(models.Model):
	user_id = models.IntegerField(max_length=11,blank=False)
	topic = models.TextField()
	more = models.TextField()
	create_time= models.DateTimeField()
	comment_count=models.IntegerField(max_length=11,default=0)
	transfer_count=models.IntegerField(max_length=11,default=0)
	subject = models.CharField(max_length=250)
	tag = models.CharField(max_length=250)
	last_update_time = models.DateTimeField()

	class Meta:
		db_table='topic'
		ordering=['-create_time']

class TopicComment(models.Model):
	topic_id = models.IntegerField(max_length=11)
	user_id = models.IntegerField(max_length=11)
	to_user_id = models.IntegerField(max_length=11)
	content=models.TextField()
	create_time = models.DateTimeField()

	class Meta:
		db_table='topic_comment'
		ordering=['-create_time']


class TopicUserRelation(models.Model):
	topic_id = models.IntegerField(primary_key=True)
	user_id = models.IntegerField(primary_key=True)
	create_time = models.DateTimeField()

	class Meta:
		db_table='topic_user_relation'
		ordering=['-create_time']


def get_certain_one_topic_comment(id):
	comments = TopicComment.objects.filter(id=id).values('id','topic_id','user_id','to_user_id','content','create_time')

	if comments:
		for i in range(0,comments.count()):
			comments[i]['user']=User.objects.filter(id=comments[i]['user_id']).values('id','nickname','role','head')[0]
			if comments[i]['to_user_id']:
				comments[i]['to_user']=User.objects.filter(id=comments[i]['to_user_id']).values('id','nickname','role','head')[0]


	return comments


def get_certain_one_topoc(id):
	topics = Topic.objects.filter(id=id).values('id','user_id','topic','more','comment_count','transfer_count','create_time','tag','subject')
	if topics:
		for i in range(0,topics.count()):
			topics[i]['user']=User.objects.filter(id=topics[i]['user_id']).values('id','nickname','role','head','url')[0]

	return topics[0]



def get_limit_topic_comments(topic_id,start=None,end=None):
	if  start>=0 and end>=start:
		comments = TopicComment.objects.filter(topic_id=topic_id)[start:end].values('id','user_id','to_user_id','content','create_time')
	else:
		comments = TopicComment.objects.filter(topic_id=topic_id).values('id','user_id','to_user_id','content','create_time')

	if comments:
		for i in range(0,comments.count()):
			comments[i]['user']=User.objects.filter(id=comments[i]['user_id']).values('id','nickname','role','head')[0]
			if comments[i]['to_user_id']:
				comments[i]['to_user']=User.objects.filter(id=comments[i]['to_user_id']).values('id','nickname','role','head')[0]


	return comments

def get_topic_comments_count(topic_id):
	return TopicComment.objects.filter(topic_id=topic_id).count()

def get_topic_total_count(user_id=None):
	if user_id:
		return Topic.objects.filter(user_id=user_id).count()

	return Topic.objects.all().count()

def get_limit_topics(user_id=None,start=None,end=None):
	if not user_id:
		data=[]
		topics = Topic.objects.filter().order_by('-last_update_time','-create_time')[start:end]
		if topics:
			for t in topics:
				one={}
				one['s']=get_c_subjects(t.subject)
				one['t']=get_c_tags(t.tag)
				one['p']=t
				one['user']=User.objects.get(id=t.user_id)
				data.append(one)

		return data


	return Topic.objects.filter(user_id=user_id)[start:end].values('id','topic','create_time','comment_count')

def get_i_college_topic_count(user_id):
	us = UserSchool.objects.get(id=user_id)
	if us.college:
		sql=" select count(*) from user_school as us,topic as a where us.college = "+str(us.college)+" and a.user_id = us.id"
		result = custom_raw_sql(sql)
		if result:
			return result[0][0]
		else:
			return 0

def get_i_college_limit_topics(user_id,start,end):
	us = UserSchool.objects.get(id=user_id)
	data=[]
	if us.college:
		sql = "select a.id,a.user_id,a.topic,a.create_time,a.comment_count,a.tag,a.subject from user_school us,topic a where us.college="+str(us.college)+" and us.id = a.user_id order by create_time desc,comment_count desc limit "+str(start)+","+str(end)+""
		topics=custom_raw_sql(sql)
		for a in topics:
			id,user_id,t,create_time,comment_count,tag,subject=a
			topic={}
			topic['id']=id
			topic['user_id']=user_id
			topic['topic']=t
			topic['comment_count']=comment_count
			topic['create_time']=create_time
			one={}
			one['s']=get_c_subjects(subject)
			one['t']=get_c_tags(tag)
			one['p']=topic
			one['user']=User.objects.get(id=user_id)
			data.append(one)

	return data