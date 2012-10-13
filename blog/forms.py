# -*- coding: utf-8 -*- 

from django import forms
from models import *
from datetime import datetime
import re
from linkusall.util import decode_data
from linkusall.subject.models import Tag,Subject,process_tags_subjects
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class ArticleForm(forms.Form):

	title = forms.CharField(error_messages={"required":"题目不能为空"}, widget=forms.TextInput(attrs={'autocomplete': 'off',}))
	content = forms.CharField(widget=forms.Textarea,required=False)
	# catalog = forms.ModelChoiceField(required=True,queryset=None,empty_label=None)
	id = forms.CharField(widget=forms.HiddenInput,required=False)

	def __init__(self,*args,**kwargs):
		self.user_id = kwargs.pop('user_id', None)
		super(ArticleForm,self).__init__(*args,**kwargs)
		# self.fields['catalog'].queryset =ArticleCatalog.objects.filter(user_id=self.user_id)
	
	

	def save(self,user_id,tags,subjects):
		try:
			tag_data,subject_data='',''
			tag_data,subject_data = process_tags_subjects(tags,subjects,user_id=user_id)

			a = Article(user_id=user_id,title=self.cleaned_data['title'],content=self.cleaned_data['content'],tag=tag_data,subject=subject_data,create_time=datetime.now())
			a.save()
		except Exception, e:
			raise
		else:
			pass
		finally:
			pass

	# def init(self,user_id):
		# self.fields['catalog'].queryset = ArticleCatalog.objects.filter(user_id=self.user_id)
		#self.fields['catalog'].choices=[(a['id'],a['catalog']) for a in ArticleCatalog.objects.filter(user_id=user_id).values('id','catalog')]
		

	def update(self,user_id,tags,subjects):
		try:
			#更新数据库对象
			tag_data,subject_data='',''
			tag_data,subject_data = process_tags_subjects(tags,subjects)

			Article.objects.filter(id=self.cleaned_data['id']).update(title=self.cleaned_data['title'],tag=tag_data,subject=subject_data,content=self.cleaned_data['content'])
		except Exception, e:
			raise
		else:
			pass
		finally:
			pass
	



class ArticleCommentForm(forms.Form):
	article_id = forms.IntegerField()
	to_user_id = forms.IntegerField(required=False)
	comment = forms.CharField(widget=forms.Textarea)

	def save(self,user_id):
		try:
			a = ArticleComment(article_id=self.cleaned_data['article_id'],user_id=user_id,to_user_id=self.cleaned_data['to_user_id'],content=re.sub(r'\n|\r','',decode_data(self.cleaned_data['comment'])),create_time=datetime.now())
			a.save()
			return a
		except Exception, e:
			raise
		else:
			pass
		finally:
			pass





