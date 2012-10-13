# -*- coding: utf-8 -*- 
# Create your views here.

from django import forms
from models import *
from datetime import datetime
import re
from linkusall.util import decode_data
from django.db import IntegrityError
from linkusall.subject.models import Tag,process_tags_subjects

class QuestionForm(forms.Form):
	question = forms.CharField(widget=forms.Textarea,error_messages={"required":"问题不能为空"})
	more = forms.CharField(widget=forms.Textarea,required=False)
	anonymity = forms.CharField(widget=forms.CheckboxInput,required=False)
	id = forms.CharField(widget=forms.HiddenInput,required=False)


	def save(self,user_id,tags,subjects):
		try:
			anony=0
			tag_data,subject_data='',''
			tag_data,subject_data = process_tags_subjects(tags,subjects,user_id=user_id)
			if self.cleaned_data['anonymity']=='on':
				anony=1

			a = Question(user_id=user_id,question=self.cleaned_data['question'],question_more=self.cleaned_data['more'],tag=tag_data,subject=subject_data,anonymity=anony,create_time=datetime.now())
			a.save()
			
			#更新用户问答数据统计
			uans = UserAskAnswerState.objects.get(id=user_id)
			UserAskAnswerState.objects.filter(id=uans.id).update(question_count=uans.question_count+1)
		except Exception, e:
			raise
		else:
			pass
		finally:
			pass

	def update(self,user_id,tags,subjects):
		anony=0
		tag_data,subject_data='',''
		tag_data,subject_data = process_tags_subjects(tags,subjects,user_id=user_id)
		if self.cleaned_data['anonymity']=='on':
				anony=1
		Question.objects.filter(id=self.cleaned_data['id']).update(question=self.cleaned_data['question'],question_more=self.cleaned_data['more'],tag=tag_data,subject=subject_data,anonymity=anony)



class AnswerForm(forms.Form):
	answer = forms.CharField(widget=forms.Textarea)
	q_id = forms.CharField(widget=forms.HiddenInput,required=False)
	a_id = forms.CharField(required=False)

	def save(self,user_id):
		try:
			a = Answer(q_id=self.cleaned_data['q_id'],user_id=user_id,answer=decode_data(self.cleaned_data['answer']),create_time=datetime.now())
			a.save()
			#更新问题答案数量
			q = Question.objects.get(id=self.cleaned_data['q_id'])
			Question.objects.filter(id=q.id).update(answer_count=q.answer_count+1,last_update_time=datetime.now())

			#更新用户问答数据统计
			uans = UserAskAnswerState.objects.get(id=user_id)
			UserAskAnswerState.objects.filter(id=uans.id).update(answer_count=uans.answer_count+1)
			return a
		except Exception, e:
			raise
		else:
			pass
		finally:
			pass

	def update(self,user_id):
		try:
			Answer.objects.filter(id=self.cleaned_data['a_id']).update(answer=decode_data(self.cleaned_data['answer']))
			return Answer.objects.get(id=self.cleaned_data['a_id'])
		except Exception, e:
			raise
		else:
			pass
		finally:
			pass