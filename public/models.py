from django.db import models
from linkusall.blog.models import Article
from linkusall.ask.models import Question
from linkusall.topic.models import Topic
from django.db.models import Q
from linkusall.subject.models import Subject
from django.db import connection,transaction
from linkusall.util import execute_subject_query


def execute_sql(id,table):
	sql = "select count(*) from "+table+"  where subject like %s or subject like %s "
	param=(str(id)+',%','%,'+str(id)+',%')
	return custome_raw_param_sql(sql,param=param)


def count_article_subjects():
	subjects= Subject.objects.all()
	for s in subjects:
		result = execute_subject_query(s.id,'article')
		Subject.objects.filter(id=s.id).update(article_count=result[0][0])

def count_question_subjects():
	subjects= Subject.objects.all()
	for s in subjects:
		result = execute_subject_query(s.id,'question')
		Subject.objects.filter(id=s.id).update(question_count=result[0][0])

def count_topic_subjects():
	subjects= Subject.objects.all()
	for s in subjects:
		result = execute_subject_query(s.id,'topic')
		Subject.objects.filter(id=s.id).update(topic_count=result[0][0])