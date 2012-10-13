# -*- coding: utf-8 -*- 

from django import forms
from models import *
from datetime import datetime
import re
from linkusall.util import decode_data
from linkusall.subject.models import Tag,Subject,process_tags_subjects

class TopicForm(forms.Form):
	topic = forms.CharField(widget=forms.Textarea)
	more = forms.CharField(widget=forms.Textarea,required=False)

	def save(self,user_id,tags,subjects):

		tag_data,subject_data='',''
		tag_data,subject_data = process_tags_subjects(tags,subjects,user_id=user_id)

		t = Topic(user_id=user_id,topic=re.sub(r'\n|\r','<br>',decode_data(self.cleaned_data['topic'])),subject=subject_data,tag=tag_data,more=re.sub(r'\n|\r','<br>',decode_data(self.cleaned_data['more'])),create_time=datetime.now())
		t.save()

		return t


class TopicCommentForm(forms.Form):
	topic_id = forms.IntegerField()
	to_user_id = forms.IntegerField(required=False)
	content = forms.CharField(widget=forms.Textarea)

	def save(self,user_id):
		try:
			a = TopicComment(topic_id=self.cleaned_data['topic_id'],user_id=user_id,to_user_id=self.cleaned_data['to_user_id'],content=re.sub(r'\n|\r','',decode_data(self.cleaned_data['content'])),create_time=datetime.now())
			a.save()
			t = Topic.objects.filter(id=self.cleaned_data['topic_id']).values('comment_count')
			#更新评论总数
			Topic.objects.filter(id=self.cleaned_data['topic_id']).update(comment_count=t[0]['comment_count']+1,last_update_time=datetime.now())

			return a
		except Exception:
			return a
		else:
			pass
		finally:
			pass
