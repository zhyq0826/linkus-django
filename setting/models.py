# -*- coding: utf-8 -*- 
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from util import * 
from datetime import datetime,date
# Create your models here.

class UserProfile(models.Model):

	GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )

	name = models.CharField(max_length=128,null=True)
	sex = models.CharField(max_length=1,null=True)
	birth = models.DateTimeField(auto_now=False,null=True)
	city = models.SmallIntegerField(null=True)
	province = models.SmallIntegerField(null=True)
	hometown = models.SmallIntegerField(null=True)
	position = models.CharField(max_length=250,null=True)
	skill = models.CharField(max_length=1000)
	favorite=models.CharField(max_length=1000)

	def get_data(self):
		
		return{
			'name':self.name,
			'sex':self.sex,
			'birth':self.birth,
			'province':self.province,
			'city':self.city,
			'hometown':self.hometown,
			'position':self.position,
			'skill':self.skill,
			'favorite':self.favorite
		}

	class Meta:
		db_table='user_profile'





class UserSchool(models.Model):
	college = models.SmallIntegerField()
	school = models.SmallIntegerField()
	start_year= models.CharField(null=True,max_length=4)
	end_year = models.CharField(null=True,max_length=4)



	def get_data(self):
		
		return{
			'college':self.college,
			'school':self.school,
			'start_year':self.start_year,
			'end_year':self.end_year
		}

	class Meta:
		db_table = 'user_school'


class Province(models.Model):
	""" 省份 """
	pid = models.AutoField(primary_key=True)
	pname  = models.CharField(max_length=50)
	provinceID = models.IntegerField(unique=True)

	class Meta:
		db_table='province'
		ordering = ["pid"]


class City(models.Model):
	""" 市以及地区 """
	cid = models.AutoField(primary_key=True)
	cityID = models.IntegerField(unique=True)
	city  = models.CharField(max_length=50)
	provinceID =models.IntegerField(unique=False)

	class Meta:
		db_table='city'
 

class Area(models.Model):
	""" 区市级以下城市 """
	aid = models.AutoField(primary_key=True)
	area = models.CharField(max_length=50)
	areaID = models.IntegerField(unique=True)
	cityID = models.IntegerField(unique=False)

	class Meta:
		db_table='area'


class College(models.Model):
	"""大学"""
	coid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	provinceID = models.IntegerField(unique=False)

	class Meta:
		db_table = 'college'


class School(models.Model):
	"""学院"""
	scid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	collegeID = models.IntegerField(unique=False)

	class Meta:
		db_table='school'


def get_user_profile(id):
	try:
		user_profile = UserProfile.objects.get(id=id)
		if user_profile:
			return user_profile
	except ObjectDoesNotExist:
		new_user_profile = UserProfile(id=id)
		new_user_profile.save()
		return new_user_profile
	else:
		pass
	finally:
		pass

def get_province(id):
	try:
		p = Province.objects.get(provinceID=id)
		if p:
			return p.pname
	except ObjectDoesNotExist:
		return ''
	else:
		pass
	finally:
		pass

def get_city(id):
	try:
		c = City.objects.get(cityID=id)
		if c:
			return c.city
	except ObjectDoesNotExist:
		return ''
	else:
		pass
	finally:
		pass

def get_area(id):
	try:
		a = Area.objects.get(areaID=id)
		if a:
			return a.area
	except ObjectDoesNotExist:
		return ''
	else:
		pass
	finally:
		pass


def get_college(id):
	try:
		c = College.objects.get(coid=id)
		if c:
			return c.name
	except ObjectDoesNotExist:
		return ''
	else:
		pass
	finally:
		pass

def get_school(id):
	try:
		s = School.objects.get(scid=id)
		if s:
			return s.name
	except ObjectDoesNotExist:
		return ''
	else:
		pass
	finally:
		pass


def get_user_school(id):
	try:
		u = UserSchool.objects.get(id=id)
		if u:
			return u
	except ObjectDoesNotExist:
		 u = UserSchool(id=id)
		 u.save()
		 return u
	else:
		pass
	finally:
		pass