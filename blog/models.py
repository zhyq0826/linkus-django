#-*- coding:utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.core.mail import send_mail
from datetime import datetime
from linkusall.auth.models import User
from linkusall.setting.models import UserSchool
from django.db.models import Q
from linkusall.util import execute_subject_query,custom_raw_sql

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

class Article(models.Model):
	user_id = models.IntegerField(max_length=11)
	title = models.CharField(max_length=300)
	content = models.TextField()
	create_time = models.DateTimeField()
	comment_count = models.IntegerField(max_length=11)
	transfer_count = models.IntegerField(max_length=11)
	subject = models.CharField(max_length=250)
	tag = models.CharField(max_length=250)

	def get_data(self):
		return{
			'id':self.id,
			'content':self.content,
			'title':self.title,
		}

	class Meta:
		db_table='article'
		ordering=['-create_time']



class ArticleComment(models.Model):
	article_id = models.IntegerField(max_length=11)
	user_id = models.IntegerField(max_length=11)
	to_user_id = models.IntegerField(max_length=11,blank=True)
	content = models.TextField()
	create_time = models.DateTimeField()

	class Meta:
		db_table = 'article_comment'
		ordering=['create_time']

def get_article(id,user_id=None):
	try:
		if user_id:
			a = Article.objects.get(id=id,user_id=user_id)
		else:
			a = Article.objects.get(id=id)
		if a:
			return a
	except ObjectDoesNotExist:
		return None

def get_author(id):
	return User.objects.get(id=id)

#查询所有id小于该文章的的文章，即早先发表的文章，后一篇的文章
def get_user_next_article(user_id,id):
	sql = "select id,title from article where user_id=%d and id < %d ORDER BY id desc limit 0,1"%(user_id,id)
	articles=custom_raw_sql(sql)
	if articles:
		one={}
		one['id']=articles[0][0]
		one['title']=articles[0][1]
		return one
	else:
		return None
#查询所有id小于该文章的的文章，即早先发表的文章，后一篇的文章
def get_subject_next_article(s_id,id):
	sql = "select id,title from article a where (subject like %s or subject like %s) and id<"+str(id)+" ORDER BY id desc limit 0,1"
	articles=execute_subject_query(s_id,sql=sql)
	if articles:
		one={}
		one['id']=articles[0][0]
		one['title']=articles[0][1]
		return one
	else:
		return None

#查询所有id小于该文章的的文章，即早先发表的文章，后一篇的文章
def get_next_article(id):
	sql = "select id,title from article where id < %d ORDER BY id desc limit 0,1"%(id)
	articles = custom_raw_sql(sql)

	if articles:
		one={}
		one['id']=articles[0][0]
		one['title']=articles[0][1]
		return one
	else:
		return None

#查询所有id大于该文章的的文章，即后来发表的文章，前一篇的文章
def get_user_prev_article(user_id,id):
	
	sql = "select id,title from article where user_id=%d and id > %d ORDER BY id asc limit 0,1"%(user_id,id)
	articles=custom_raw_sql(sql)
	if articles:
		one={}
		one['id']=articles[0][0]
		one['title']=articles[0][1]
		return one
	else:
		return None

def get_subject_prev_article(s_id,id):
	
	sql = "select id,title from article a where (subject like %s or subject like %s) and id>"+str(id)+" ORDER BY id asc limit 0,1"
	articles=execute_subject_query(s_id,sql=sql)
	if articles:
		one={}
		one['id']=articles[0][0]
		one['title']=articles[0][1]
		return one
	else:
		return None

def get_prev_article(id):
	
	sql = "select id,title from article where id > %d ORDER BY id asc limit 0,1"%(id)
	articles = custom_raw_sql(sql)

	if articles:
		one={}
		one['id']=articles[0][0]
		one['title']=articles[0][1]
		return one
	else:
		return None

def get_articles(user_id):
	return Article.objects.filter(user_id=user_id).values('id','title','create_time')

def get_articles_by_subject(id,start=None,end=None):
	data=[]
	sql = "select id,user_id,title,content,create_time from article a where subject like %s or subject like %s order by create_time desc limit "+str(start)+","+str(end)+""
	articles=execute_subject_query(id,sql=sql)
	for a in articles:
		a_id,user_id,title,content,create_time=a
		article={}
		article['id']=a_id
		article['user_id']=user_id
		article['title']=title
		article['content']=content
		article['create_time']=create_time
		one = {}
		one['article']=article
		one['author']=User.objects.get(id=user_id)
		data.append(one)

	return data

def get_articles_by_comment_recommended(start=None,end=None):
	data=[]
	articles = Article.objects.filter()[start:end]
	if articles:
		for a in articles:
			one={}
			one['article']=a
			one['author']=User.objects.get(id=a.user_id)
			data.append(one)

	return data

#某个主题的文章总量
def get_some_subject_article_count(id):
	return execute_subject_query(id,'article')[0][0]


#根据用户和分类来统计文章总数
def get_article_total_count(user_id=None):
	if not user_id:
		return Article.objects.all().count()
	return Article.objects.filter(user_id=user_id).count()

#返回指定数量的文章
def get_limit_articles(user_id,start,end):
	return Article.objects.filter(user_id=user_id)[start:end].values('id','title','content','create_time')


#统计文章评论数量
def get_article_comments_count(article_id):
	return ArticleComment.objects.filter(article_id=article_id).count()


#获取指定数量的评论
def get_limit_comments(article_id,start=None,end=None):
	comments = ArticleComment.objects.filter(article_id=article_id)[start:end]
	data={}
	if comments:
		for i in range(0,comments.count()):
			try:
				one={}
				one['comment']=comments[i]
				one['user'] = User.objects.get(id=comments[i].user_id)
				if comments[i].to_user_id:
					one['to_user']=User.objects.get(id=comments[i].to_user_id)
				data[i] = one		
			except ObjectDoesNotExist:
				pass

	return sort_dict_values(data)


#取得一片文章的评论
def get_article_comments(id):
	comments =  ArticleComment.objects.filter(article_id=id)
	data={}
	if comments:
		for i in range(0,comments.count()):
			try:
				one={}
				one['comment']=comments[i]
				one['user'] = User.objects.get(id=comments[i].user_id)
				if comments[i].to_user_id:
					one['to_user']=User.objects.get(id=comments[i].to_user_id)
				data[i] = one		
			except ObjectDoesNotExist:
				pass

	return sort_dict_values(data)



#提取一篇文章的某一条评论
def get_atcile_comment(id):
	one={}
	try:
		comment = ArticleComment.objects.get(id=id)
		one['comment']=comment
		one['user'] = User.objects.get(id=comment.user_id)
		if comment.to_user_id:
			one['to_user']=User.objects.get(id=comment.to_user_id)
		return one
	except Exception, e:
		return one
	else:
		pass
	finally:
		pass
		



#因为字典是无序的，先进行排序
def sort_dict_values(adict):
	if adict:	
		keys = adict.keys()
		keys.sort()
		return [(key,adict[key]) for key in keys]

	return adict


def get_i_college_article_count(user_id):
	us = UserSchool.objects.get(id=user_id)
	if us.college:
		sql=" select count(*) from user_school as us,article as a where us.college = "+str(us.college)+" and a.user_id = us.id"
		result = custom_raw_sql(sql)
		if result:
			return result[0][0]
		else:
			return 0

def get_articles_by_i_college(user_id,start,end):
	us = UserSchool.objects.get(id=user_id)
	data=[]
	if us.college:
		sql = "select a.id,a.user_id,a.title,a.create_time,a.content from user_school us,article a where us.college="+str(us.college)+" and us.id = a.user_id order by create_time desc limit "+str(start)+","+str(end)+""
		articles=custom_raw_sql(sql)
		for a in articles:
			a_id,user_id,title,create_time,content=a
			article={}
			article['id']=a_id
			article['user_id']=user_id
			article['title']=title
			article['content']=content
			article['create_time']=create_time
			one = {}
			one['article']=article
			one['author']=User.objects.get(id=user_id)
			data.append(one)

	return data
