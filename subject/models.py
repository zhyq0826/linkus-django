from django.db import models
import json
from django.db import IntegrityError
from datetime import datetime
from linkusall.util import custom_raw_sql as execute_sql
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class Subject(models.Model):
	subject = models.CharField(max_length=250)
	create_time = models.DateTimeField()
	focus_count = models.IntegerField(max_length=11,default=0)
	brief=models.TextField()
	article_count = models.IntegerField(max_length=11)
	question_count = models.IntegerField(max_length=11)
	topic_count = models.IntegerField(max_length=11)


	class Meta:
		db_table='subject'


class Tag(models.Model):
	tag = models.CharField(max_length=250)
	create_time = models.DateTimeField()
	focus_count = models.IntegerField(max_length=11,default=0)
	user_id = models.IntegerField(max_length=11)
	brief=models.TextField()


	class Meta:
		db_table='tag'

def get_subjects():
	return Subject.objects.all()

def get_one_subject(id):
	try:
		one = Subject.objects.get(id=id)
		if one:
			return one
		else:
			return None
	except ObjectDoesNotExist:
		return None
	else:
		pass
	finally:
		pass

def search_tags(q):

	results = Tag.objects.filter(tag__icontains=q).values('id','tag')
	data = []
	one={}
	for i in results:
		one['key']=i['id']
		one['value']=i['tag']
		data.append(one)

	return json.dumps(data,separators=(',',':'),encoding='utf-8')


def get_c_tags(tags):
	one={}
	tag_data=[]
	data=[]
	if tags:
		tag_data = tags.split(',')
		data = Tag.objects.filter(id__in=tag_data[0:-1])
		return data

def get_c_subjects(subjects):
	one={}
	subject_data=[]
	data=[]
	if subjects:
		subject_data = subjects.split(',')

		data = Subject.objects.filter(id__in=subject_data[0:-1])
		return data		


def process_tags_subjects(tags,subjects,user_id=None):
		tag_data=''
		if tags:
			for i in range(0,len(tags)):
				if tags[i].strip().startswith('-'):
					try:
						t = Tag(tag=tags[i].strip()[1:],create_time=datetime.now(),user_id=user_id)
						t.save()
						tags[i]=t.id
					except IntegrityError:
						t = Tag.objects.filter(tag=tags[i].strip()[1:])
						if len(t)>0:
							tags[i]=t[0].id
						else:
							tags.pop(i)
					else:
						pass
					finally:
						pass
					

			for v in tags:
			    tag_data+=str(v)+','

		subject_data=''
		if subjects:
			for v in subjects:
				subject_data+=str(v)+','

		return tag_data,subject_data