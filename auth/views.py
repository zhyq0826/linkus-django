# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect

from forms import *
from models import *


from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.template import TemplateDoesNotExist,Template,Context
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt


import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

#注册
def register(request,template_name='auth/register.html'):
	errors={'email_existed':'','nickname_existed':''}
	G={}
	try:
		pagetitle='注册'
		if request.method=='GET':
			form = RegisterForm(auto_id='%s')
			return render_to_response(template_name,{'form':form,'pagetitle':pagetitle})
		else:
			form = RegisterForm(request.POST,auto_id='%s')
			if form.is_valid():
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']
				nickname = form.cleaned_data['nickname']
				role = form.cleaned_data['role']

				if is_registered(email):
					errors['email_existed']='账号已经注册'
				if is_registered_nickname(nickname):
					errors['nickname_existed']='昵称已经存在'


				if errors['email_existed'] or errors['nickname_existed']:
					return render_to_response(template_name,{'form':form,'errors':errors,'pagetitle':pagetitle})
				else:
					#用户注册
					user_apply = apply(email,password,nickname)
					#发送邮件
					user_apply.sendemail(email)
					G['email']=email
					return render_to_response(template_name,{'G':G})
			else:
				return render_to_response(template_name,{'form':form,'pagetitle':pagetitle})

	except TemplateDoesNotExist:
		raise
	else:
		pass
	finally:
		pass

#激活
def active(request,template_name='auth/active.html',email=None,ck=None):
	errors={}
	G={}
	try:
		pagetitle='账户激活'
		if email and ck:
			#是否已经注册
			if is_registered(email):
				#是否是待激活邮箱
				apply_user = is_applyed(email)
				if apply_user:
					if apply_user.verify(ck):						
						id = apply_user.id
						#激活账户
						create_user(id)
						G['actived']=True
						return render_to_response(template_name,{'G':G,'pagetitle':pagetitle})
					else:
						G['ck_error']=True
						return render_to_response(template_name,{'G':G,'pagetitle':pagetitle})
				elif is_actived_member(email):
					#账户已经激活
					G['created']=True
					return render_to_response(template_name,{'G':G,'pagetitle':pagetitle})
			else:
				#邮箱尚未注册
				G['no_existed']=True
				return render_to_response(template_name,{'G':G,'pagetitle':pagetitle})
		else:
			G['error']=True
			return render_to_response(template_name)

	except TemplateDoesNotExist:
		raise
	else:
		pass
	finally:
		pass


def reset_pw_apply(request,template_name='auth/reset_password_apply.html'):
	errors={}
	G={}
	try:
		pagetitle='重置密码'
		if request.method=='GET':
			form = ResetPasswordApplyForm(auto_id='%s')
			G['reseted']=False
			return render_to_response(template_name,{'form':form,'G':G,'pagetitle':pagetitle})
		else:
			form = ResetPasswordApplyForm(request.POST,auto_id='%s')
			if form.is_valid():
				email = form.cleaned_data['email']
				registered_user= is_registered(email)
				if registered_user:
					reset_password_apply(registered_user.id,email)
					G['reseted']=True
					G['email']=email
					return render_to_response(template_name,{'G':G,'pagetitle':pagetitle})
				else:
					G['reseted']=False
					errors['no_existed']='邮箱尚未注册'
					return render_to_response(template_name,{'form':form,'errors':errors,'G':G,'pagetitle':pagetitle},)
			else:
				G['reseted']=False
				return render_to_response(template_name,{'form':form,'G':G,'pagetitle':pagetitle},)

	except TemplateDoesNotExist:
		raise
	else:
		pass
	finally:
		pass


def reset_pw(request,template_name='auth/reset_password.html',id=None,ck=None):
	errors={}
	G={}
	try:
		pagetitle='重置密码'
		if id  and ck and id.isdigit():
			id = int(id)
			#是否申请过重置密码
			urp = is_reset_password_apply(id)
			if urp:
				if request.method=='GET':
					form = ResetPasswordForm(auto_id='%s')
					G['reseted']=False
					return render_to_response(template_name,{'form':form,'G':G,'pagetitle':pagetitle})
				else:
					form = ResetPasswordForm(request.POST,auto_id='%s')
					if form.is_valid():
						password = form.cleaned_data['newpassword']
						if urp.verify(ck):
							G['reseted']=True
							reset_password(id,password)
							return render_to_response(template_name,{'G':G,'pagetitle':pagetitle})
						else:
							G['reseted']=True
							G['wrong']=True
							return render_to_response(template_name,{'G':G,'pagetitle':pagetitle})
					else:
						G['reseted']=False
						return render_to_response(template_name,{'form':form,'pagetitle':pagetitle})

			else:
				G['reseted']=True
				G['wrong']=True
				return render_to_response(template_name,{'G':G})
		else:
			G['reseted']=True
			G['wrong']=True
			return render_to_response(template_name,{'G':G})
	except TemplateDoesNotExist:
		raise
	else:
		pass
	finally:
		pass

@csrf_exempt
def login(request,template_name='auth/login.html'):
	errors={}
	G={}
	try:
		if template_name=='index.html':
			pagetitle='首页'
		else:
			pagetitle='登陆' 

		if request.method=='GET':
			form = LoginForm(auto_id='%s')
			return render_to_response(template_name,{'form':form,'pagetitle':pagetitle})
		else:
			form = LoginForm(request.POST,auto_id='%s')
			if form.is_valid():
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']

				actived_user = is_actived_member(email)
				#是已经激活的用户,验证密码
				if actived_user:
					if verify_password(actived_user.id,password):
						#密码正确转到主页
						#设置cookie到期时间

						if form.cleaned_data['remember']=='on':
							# t=Template('{{ value }}')
							# html = t.render(Context({'value':form.cleaned_data['remember']}))
							# return HttpResponse(html)
							request.session.set_expiry(None)
						else:
							request.session.set_expiry(0)
						#登陆用户
						request.session['user']=actived_user
						#当前访问主页的用户
						request.session['current_user']=actived_user
						return redirect('/read/')
						# if actived_user.url:
						# 	return redirect('/people/'+actived_user.url+'')
						# else:
						# 	use_id = str(actived_user.id)
						# 	return redirect('/people/'+use_id+'')
					else:
						# errors['password_wrong']='密码错误'
						errors['wrong']='用户名或密码错误'
						return render_to_response(template_name,{'form':form,'errors':errors,'pagetitle':pagetitle})
				else:
					errors['wrong']='用户名或密码错误'
					return render_to_response(template_name,{'form':form,'errors':errors,'pagetitle':pagetitle})

				# #不是已经激活的用户,但是是注册用户
				# elif is_registered(email):
				# 	#是否是待激活邮箱
				# 	apply_user = is_applyed(email)
				# 	if apply_user:
				# 		errors['unactive']='账户未激活'
				# 		return render_to_response(template_name,{'form':form,'errors':errors,'pagetitle':pagetitle})
				# else:
				# 	errors['unregisted']='邮箱未注册'
				# 	return render_to_response(template_name,{'form':form,'errors':errors,'pagetitle':pagetitle})
			else:
				return render_to_response(template_name,{'form':form,'pagetitle':pagetitle})
	except KeyError:
		raise Http404()
	else:
		pass
	finally:
		pass

def logout(request):
	try:
		del request.session['user']
		del request.session['current_user']
		return redirect('/')
	except Exception, e:
		return redirect('/')

	