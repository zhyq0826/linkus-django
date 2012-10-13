# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext,Template, Context
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
from forms import *
from models import *
from django.utils.encoding import force_unicode
from django.conf import settings

from django.http import Http404,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError
import os,ImageFile,uuid,Image
from linkusall.auth.models import get_user
from linkusall.util import random_char
from django.views.decorators.csrf import csrf_exempt
import sys 
import re
reload(sys) 
sys.setdefaultencoding('utf8')


def check_nick_name(nickname):
	re_nickname=re.compile(u'^[0-9a-zA-Z\u4e00-\u9fa5]{2,12}$', re.UNICODE)
	s = force_unicode(nickname)
	m = re_nickname.search(s)
	if not m:
		return False
	else:
		return True 

def check_url(url):
	re_url = re.compile(r'^[0-9a-zA-Z]{4,20}$',re.UNICODE)
	m = re_url.search(url)
	if not m:
		return False
	else:
		return True


def setting(request,template_name='setting/setting.html'):
	try:
		u = request.session['user']
		errors={}
		G={}
		if request.method=='GET':
			data={'nickname':u.nickname,'blog':u.blog,'url':u.url,'signature':u.signature}
			form = UserForm(data,auto_id='%s')
			return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
		else:
			form = UserForm(request.POST,auto_id='%s')
			if form.is_valid():
				nickname = form.cleaned_data['nickname']
				if not check_nick_name(nickname):
					errors['ni_error']='昵称2-12位，支持中文，数字，字母'
					return render_to_response(template_name,{'form':form,'errors':errors},context_instance=RequestContext(request))	
				form.update(u.id)
				u = get_user(u.id)
				request.session['user']=u
				G['success']='success'
				return render_to_response(template_name,{'form':form,'G':G},context_instance=RequestContext(request))
			else:
				return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))

	except Exception, e:
		raise 
	else:
		pass
	finally:
		pass

def setting_url(request,template_name='setting/setting_url.html'):
	try:
		u = request.session['user']
		errors={}
		G={}
		if request.method=='GET':
			data={'url':u.url}
			form = UserUrl(data,auto_id='%s')
			return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
		else:
			form = UserUrl(request.POST,auto_id='%s')
			if form.is_valid():
				url = form.cleaned_data['url']
				if not check_url(url):
					errors['url_error']='个性域名必须由4-20位数字和字母组成'
					return render_to_response(template_name,{'form':form,'errors':errors},context_instance=RequestContext(request))	
				form.update(u.id)
				u = get_user(u.id)
				request.session['user']=u
				G['success']='success'
				return render_to_response(template_name,{'form':form,'G':G},context_instance=RequestContext(request))
			else:
				return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))


	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def setting_profile(request,template_name='setting/setting_profile.html'):
	try:
		u = request.session['user']
		user_profile = get_user_profile(u.id)
		if user_profile:
			provinceID = user_profile.province
			cityID = user_profile.city
			hometown = user_profile.hometown
			pname,cname,aname='---','---','---'
			if provinceID:
				pname = get_province(provinceID)

			if cityID:
				cname = get_city(cityID)

			if hometown:
				aname = get_area(hometown)

			if request.method=='GET':
				#初始化form
				form = UserProfileForm(user_profile.get_data(),auto_id='%s')
				data ={'form':form,'pname':pname,'cname':cname,'aname':aname,'provinceID':provinceID,'cityID':cityID}
				return render_to_response(template_name,data,context_instance=RequestContext(request))
			else:
				form = UserProfileForm(request.POST,auto_id='%s')
				data ={'form':form,'pname':pname,'cname':cname,'aname':aname,'provinceID':provinceID,'cityID':cityID}
				if form.is_valid():
					form.save(u.id)
					t = Template("{status:true}")
					html = t.render(Context()) 
					return HttpResponse(html)
				else:
					t = Template("{status:false}")
					html = t.render(Context()) 
					return HttpResponse(html)
		else:
			return redirect('/i/setting/')
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass

#学校信息设置
#取得学校信息，如果有的话
def setting_school(request,template_name='setting/setting_school.html'):
	try:

		u = request.session['user']
		user_school = get_user_school(u.id)
		if user_school:
			collegeId = user_school.college
			schoolId = user_school.school
			start = user_school.start_year
			end = user_school.end_year
			schools=None
			cname,sname='---','---'
			if collegeId:
				cname = get_college(collegeId)
				schools = School.objects.filter(collegeID=collegeId)

			if schoolId:
				sname = get_school(schoolId)

			if start:
				pass
			else:
				start='---'

			if end:
				pass
			else:
				end='---'

			school_years=[]
			for i in range(2005,2025):
				school_years.append(i)


			if request.method=='GET':
				form = UserSchoolForm(user_school.get_data(),auto_id='%s')
				data={'form':form,'cname':cname,'sname':sname,'start':start,'end':end,'school_years':school_years,'schools':schools}
				return render_to_response(template_name,data,context_instance=RequestContext(request))
			else:
				form = UserSchoolForm(request.POST,auto_id='%s')
				data={'form':form,'cname':cname,'sname':sname,'start':start,'end':end,'school_years':school_years}
				if form.is_valid():
					form.save(u.id)
					t = Template("{'status':'true'}")
					html = t.render(Context()) 
					return HttpResponse(html)
				else:
					t = Template("{'status':'false'}")
					html = t.render(Context()) 
					return HttpResponse(html)
		else:
			t = Template("{'status':'false'}")
			html = t.render(Context()) 
			return HttpResponse(html)
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass


def getcollege(request,id):

	id = int(id)
	colleges = College.objects.filter(provinceID=id)

	t = Template("{% autoescape on %} {% for college in colleges %}<li><a onclick='catch_school(this,{{ college.coid }})'  href='#'>{{ college.name }}</a></li>{% endfor %}{% endautoescape %}")

	html = t.render(Context({'colleges':colleges}))

	return HttpResponse(html)



def getschool(request,id):
	id = int(id)
	schools = School.objects.filter(collegeID=id)

	t = Template("{% autoescape on %} {% for school in schools %}<li onclick='set_school({{school.scid}})' >{{ school.name }}</li>{% endfor %}{% endautoescape %}")
	html = t.render(Context({'schools':schools}))

	return HttpResponse(html)



# def getarea(request,id):
	
# 	id = int(id)
# 	areas = Area.objects.filter(cityID=id)

# 	t = Template("{% autoescape on %} {% for area in areas %}<li onclick='set_area({{area.areaID}})' >{{ area.area }}</li>{% endfor %}{% endautoescape %}")
# 	html = t.render(Context({'areas':areas}))

# 	return HttpResponse(html)



def setting_account(request,template_name='setting/setting_account.html'):
	errors={}
	G={}
	try:
		u = request.session['user']
		if request.method=='GET':
			form = UserAccountForm(auto_id='%s')
			return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
		else:
			form = UserAccountForm(request.POST,auto_id='%s')
			if form.is_valid():
				errors=form.verify(u.id)
				if errors:
					return render_to_response(template_name,{'form':form,'errors':errors},context_instance=RequestContext(request))
				else:
					form.change_account(u.id)
					G['success']=True
					# return redirect('/setting/')
					return  render_to_response(template_name,{'form':form,'G':G},context_instance=RequestContext(request))	
			else:
				return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass

def setting_password(request,template_name='setting/setting_password.html'):
	try:
		u = request.session['user']
		G={}
		errors={}
		if request.method=='GET':
			form = PasswordForm(auto_id='%s')
			return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
		else:
			form = PasswordForm(request.POST,auto_id='%s')
			if form.is_valid():
				if form.verify_newpassword():
					if form.verify(u.id):
						form.change_password(u.id)
						G['success']=True
						# return redirect('/setting/')
						return  render_to_response(template_name,{'form':form,'G':G},context_instance=RequestContext(request))
					else:
						errors['incorrect']='旧密码不正确'
						return render_to_response(template_name,{'form':form,'errors':errors},context_instance=RequestContext(request))
				else:
					errors['newpwerror']='新密码不一致'
					return render_to_response(template_name,{'form':form,'errors':errors},context_instance=RequestContext(request))
			else:
				return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
	except Exception,e:
		raise
	else:
		pass
	finally:
		pass


@csrf_exempt
def setting_avatar(request,template_name="setting/avatar.html"):
	u = request.session['user']
	if request.method=="GET":
		return render_to_response(template_name,context_instance=RequestContext(request))
	else:
		form = UserHeadForm(request.POST,request.FILES)
		if form.is_valid():
			path_file,status = handle_avatar_temp(request.FILES['avatarImage'],u.id)
			if status:
				t = Template("{status:true,imgurl:'"+path_file+"'}")
				html = t.render(Context()) 
				return HttpResponse(html)
			else:
				t = Template("{status:false,error:'上传失败'}")
				html = t.render(Context()) 
				return HttpResponse(html)
		else:
			return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))


@csrf_exempt
def setting_crop_avatar(request):
	try:
		u = request.session['user']
		if request.method=="POST":
			x1 = request.POST.get('x1')
			y1 = request.POST.get('y1')
			x2 = request.POST.get('x2')
			y2 = request.POST.get('y2')
			filename = request.POST.get('filename')
			try:
				x1 = float(x1)
				x2 = float(x2)
				y1 = float(y1)
				y2 = float(y2)
			except Exception, e:
				raise
			cordinate=(x1,y1,x2,y2)
			avatar_name=handle_avatar(filename,cordinate)
			update_user_avatar(u.id,avatar_name[0],avatar_name[1],filename)
			request.session['user']=get_user(u.id)
			return redirect('/setting/')
		else:
			raise 
	except Exception, e:
		raise
	

def handle_avatar_temp(imagefile,id=None):
	if imagefile:
		now = datetime.now()
		img=None
		path=os.path.join(settings.MEDIA_ROOT,'avatar/temp')
		file_name=str(uuid.uuid1())+".jpg"
		path_file=os.path.join(path,file_name)
		parser=ImageFile.Parser()
		if imagefile.multiple_chunks():
			for chunk in imagefile.chunks():
				parser.feed(chunk)
			img = parser.close()
		else:
			parser.feed(imagefile.read())
			img = parser.close()

		#resize the image
		avatar=img.resize((340,340),Image.ANTIALIAS)
		try:
			if avatar.mode!="RGB":
				avatar = avatar.convert("RGB")
			avatar.save(path_file,'jpeg',quality=100)
		except Exception, e:
			return file_name,False
			
		return file_name,True

	return None,False


def handle_avatar(imagefile,cordinate=None):
	if imagefile:
		path=os.path.join(settings.MEDIA_ROOT,'avatar/temp')
		path_file=os.path.join(path,imagefile)

		now = datetime.now()
		t = "%d%d%d%d%d%d"%(now.year,now.month,now.day,now.hour,now.minute,now.second)

		try:
		    #open image
		    img = Image.open(path_file)
		except IOError:
		    return None


		#crop image
		crop_img= img.crop(cordinate)

		#new_name
		avatar_name=random_char(3)+t+random_char(3)
		thubnail_name = avatar_name+"thumb"+".jpg"
		avatar_name = avatar_name+".jpg"

		path = os.path.join(settings.MEDIA_ROOT,'avatar')
		path_file = os.path.join(path,avatar_name)

		#resize image 120 120
		avatar_image=crop_img.resize((160,160),Image.ANTIALIAS)
		try:
		    avatar_image.save(path_file,"jpeg",quality=100)
		except Exception, e:
		    return None


		#produce thumbnail
		thumbnail =avatar_image.resize((48,48),Image.ANTIALIAS)
		path_file = os.path.join(path,thubnail_name)

		try:
		    thumbnail.save(path_file,"jpeg",quality=100)
		except Exception, e:
		    return None

		return [avatar_name,thubnail_name]


def profile(request,template_name="home/profile.html"):
	u = request.session['current_user']
	return render_to_response(template_name,context_instance=RequestContext(request))

        
		




