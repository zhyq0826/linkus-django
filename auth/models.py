# -*- coding: utf-8 -*- 
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from base64 import urlsafe_b64encode, urlsafe_b64decode
from linkusall.util import random_char,hash_password
from linkusall.blog.models import *

from django.core.mail import send_mail
from datetime import datetime,date


import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 
# Create your models here.




# from datetime import datetime
# from time import strftime,mktime
# #
# # Custom field types in here.
# #
# class UnixTimestampField(models.DateTimeField):
#     """UnixTimestampField: creates a DateTimeField that is represented on the
#     database as a TIMESTAMP field rather than the usual DATETIME field.
#     """
#     __metaclass__ = models.SubfieldBase

#     def __init__(self, null=False, blank=False, **kwargs):
#         super(UnixTimestampField, self).__init__(**kwargs)
#         # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
#         # cheat a little:
#         self.blank, self.isnull = blank, null
#         self.null = True # To prevent the framework from shoving in "not null".
        
#     def db_type(self):
#         typ=['TIMESTAMP']
#         # See above!
#         if self.isnull:
#             typ += ['NULL']
#         if self.auto_created:
#             typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
#         return ' '.join(typ)
    
#     def to_python(self, value):
#         return datetime.fromtimestamp(value)

#     def get_prep_value(self, value):
#         if value==None:
#             return None
#         return mktime(value.timetuple())

#     def get_db_prep_value(self, value):
#         if value==None:
#             return None
#         return value


class BinaryField(models.Field):
	def __init__(self,*args,**kwargs):
		super(BinaryField,self).__init__(*args,**kwargs)

	def db_type(self,connection):
		return 'binary'



class UserEmail(models.Model):
	email = models.CharField(max_length=128)


	class Meta:
		db_table='user_email'



class UserPassword(models.Model):
	password = BinaryField()

	def verify(self,password):
		p = self.password
		return p == hash_password(self.id,password)

	def change_password(self,password):
		pw=hash_password(self.id,password)
		self.password = pw
		self.save()

	class Meta:
		db_table='user_password'



class UserResetPassword(models.Model):
	ck = models.CharField(max_length=6)
	time = models.DateTimeField(auto_now=True)

	def sendemail(self,email):
		subject ='linkus，密码重置'
		ck = urlsafe_b64encode(self.ck)
		message = """
		%s,你好:
		请在七天内点击下面的链接来重置你的密码。
		http://univspot.com/accounts/resetpassword/%s/%s"""%(email,self.id,ck)
		send_mail(subject=subject,message=message,from_email='yongqiang.zhao@qq.com',recipient_list=[email],fail_silently=False)
	

	def verify(self,ck):
		return urlsafe_b64encode(self.ck)==ck	

	class Meta:
		db_table = 'user_reset_password'



class UserApply(models.Model):
	
	ck = models.CharField(max_length=6)
	time = models.DateTimeField(auto_now=True)
	nickname = models.CharField(max_length=128)
	role = models.CharField(max_length=1)

	def sendemail(self,email):
		subject ='欢迎注册，linkus，请验证你的邮箱'
		ck = urlsafe_b64encode(self.ck)
		message = """
		%s,你好:
		%s在linkus申请注册，
		这是我们的确认邮件。 
		请在七天内点击下面的链接来验证你的邮箱。
		http://127.0.0.1:8000/accounts/active/%s/%s"""%(self.nickname,email,email,ck)
		send_mail(subject=subject,message=message,from_email='yongqiang.zhao@qq.com',recipient_list =[email],fail_silently=False)
	
	def verify(self,ck):
		return urlsafe_b64encode(self.ck)==ck	

	class Meta:
		db_table = 'user_applay'



class User(models.Model):
	nickname = models.CharField(max_length=128)
	role = models.CharField(max_length=1)
	date_joined = models.DateTimeField()
	is_active=models.IntegerField(max_length=1)
	last_logined = models.DateTimeField(auto_now=True)
	last_logout = models.DateTimeField(auto_now=True)
	head = models.CharField(max_length=128)
	avatar=models.CharField(max_length=128)
	signature = models.TextField()
	blog = models.CharField(max_length=128)
	url = models.CharField(max_length=32)
	last_avatar=models.CharField(max_length=128)



	class Meta:
		db_table='user'


#邮箱是否已经注册
def is_registered(email):
	try:
		e = UserEmail.objects.get(email=email)
		if e:
			return e
	except ObjectDoesNotExist:
		return False
	else:
		pass
	finally:
		pass

def is_registered_nickname(nickname):
	try:
		e = User.objects.get(nickname=nickname)
		if e:
			return e
	except ObjectDoesNotExist:
		return False
	else:
		pass
	finally:
		pass

#是否已经激活成为正式用户
def is_actived_member(email):
	try:
		e = UserEmail.objects.get(email=email)
		if e:
			id = str(e.id)
			try:
				p = UserPassword.objects.get(id=id)
				if e and p:
					u = User.objects.get(id=id)
					return u
			except ObjectDoesNotExist:
				return False
			else:
				pass
			finally:
				pass
	except ObjectDoesNotExist:
		return False
	else:
		pass
	finally:
		pass



	
#是否申请注册但还未激活
def is_applyed(email):
	try:
		e = UserEmail.objects.get(email=email)
		if e:
			id= str(e.id)
			try:
				applyed_user = UserApply.objects.get(id=id)
				if applyed_user:
					return applyed_user
			except ObjectDoesNotExist:
				return False
			else:
				pass
			finally:
				pass

	except ObjectDoesNotExist:
		return False
	else:
		pass
	finally:
		pass




#创建激活用户
def create_user(id):
	try:
		applyed_user = UserApply.objects.get(id=id)
		if applyed_user:
			try:
				user = User.objects.get(id=id)
			except ObjectDoesNotExist:
				#激活用户并创建
				user = User(id=id)
				user.nickname = applyed_user.nickname
				user.role = applyed_user.role
				user.is_active=1
				user.date_joined = datetime.now()
				user.save()



				#todo 初始化用户问答状态
				
				
				#删除已经激活的用户申请信息
				applyed_user.delete()

				return user
			else:
				pass
			finally:
				pass
			
	except ObjectDoesNotExist:
		pass
	else:
		pass
	finally:
		pass


#验证密码
def verify_password(id,password):
	try:
		p = UserPassword.objects.get(id=id)
		if p:
			if p.verify(password):
				return True
			else:
				return False
	except ObjectDoesNotExist:
		raise
	else:
		pass
	finally:
		pass

	
#注册用户
def apply(email,password,nickname):
	email = email.lower()
	try:
		e = UserEmail.objects.get(email=email)
		if e:
			id = e.id			
	except ObjectDoesNotExist:

		#创建新的注册用户
		e = UserEmail(email=email)
		e.save()
		id = e.id

		
	else:
		pass
	finally:


		#创建用户密码
		password = hash_password(id,password)
		user_password = UserPassword(id=id,password=password)
		user_password.save()


		#生成随机key
		ck = random_char()

		try:
			apply_user = UserApply.objects.get(id=id)
		except ObjectDoesNotExist:
			apply_user = UserApply(id=id)

		finally:
			apply_user.ck = ck
			apply_user.time=datetime.now()
			apply_user.nickname = nickname
			apply_user.save()

			return apply_user

#是否是申请重置密码用户		
def is_reset_password_apply(id):
	try:
		urp = UserResetPassword.objects.get(id=id)
		if urp:
			return urp
	except ObjectDoesNotExist:
		return False
	else:
		pass
	finally:
		pass

#重置密码申请
def reset_password_apply(id,email):
	ck = random_char()
	urp = UserResetPassword(id=id,ck=ck)
	urp.save()
	urp.sendemail(email)

	return urp


#重置密码
def reset_password(id,password):
	try:
		urp=UserResetPassword.objects.get(id=id)
		if urp:
			id = urp.id
			urp.delete()	
			pw = hash_password(id,password)
			p =  UserPassword(id=id,password=pw)
			p.save()
			
	except ObjectDoesNotExist:
		raise
	else:
		pass
	finally:
		pass
	
def get_user(id):
	try:
		id = int(id)
		if id:
			try:
				u = User.objects.get(id=id)
				if u:
					return u
			except ObjectDoesNotExist:
				return None
	except ValueError:
		try:
			u = User.objects.get(url=id)
			if u:
				return u
		except ObjectDoesNotExist:
			return None


	return None
		 












