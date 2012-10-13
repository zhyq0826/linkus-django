# -*- coding: utf-8 -*- 
from auth.models import UserPassword,UserEmail,User
from models import *
from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.core.exceptions import ObjectDoesNotExist
import re
from linkusall.util import decode_data


class CustomeRadioRenderer(forms.widgets.RadioFieldRenderer):
	def render(self):
		"""Outputs a <ul> for this set of radio fields."""
		return mark_safe(u'\n%s\n' % u'\n'.join([u'%s'% force_unicode(w) for w in self]))



class UserForm(forms.Form):
	nickname = forms.CharField()
	blog = forms.URLField(error_messages={'invalid':'请输入有效的博客地址'},widget=forms.TextInput(attrs={'autocomplete':'off','placeholder':'http://'}),required=False)
	signature=forms.CharField(widget=forms.Textarea,required=False)
	


	def update(self,use_id):
		User.objects.filter(id=use_id).update(nickname=self.cleaned_data['nickname'],blog=self.cleaned_data['blog'],signature=self.cleaned_data['signature'])

class UserUrl(forms.Form):
	url = forms.CharField(required=False)

	def update(self,use_id):
		User.objects.filter(id=use_id).update(url=self.cleaned_data['url'])


class UserProfileForm(forms.Form):

	GENDER_CHOICES = (
        (u'M', u'女生'),
        (u'F', u'男生'),
    )

	name= forms.CharField(required=False,widget = forms.TextInput(attrs = {'class':'text'}))
	sex = forms.ChoiceField(widget=forms.RadioSelect(renderer=CustomeRadioRenderer),choices=GENDER_CHOICES)
	birth = forms.DateField(required=False,widget = forms.TextInput(attrs = {'class':'text'}),error_messages={"invalid":"日期格式有误"})
	province = forms.IntegerField(widget=forms.HiddenInput,required=False)
	city = forms.IntegerField(widget=forms.HiddenInput,required=False)
	hometown = forms.IntegerField(widget=forms.HiddenInput,required=False)
	position = forms.CharField(required=False,widget = forms.TextInput(attrs = {'class':'text'}))
	skill = forms.CharField(widget=forms.Textarea(),required=False)
	favorite = forms.CharField(widget=forms.Textarea(),required=False)


	def save(self,id):
		u = UserProfile(id=id,name=self.cleaned_data['name'],
			sex = self.cleaned_data['sex'],
			birth=self.cleaned_data['birth'],
			province = self.cleaned_data['province'],
			city = self.cleaned_data['city'],
			hometown = self.cleaned_data['hometown'],
			position=re.sub(r'\n|\r','',decode_data(self.cleaned_data['position'])),
			skill=re.sub(r'\n|\r','',decode_data(self.cleaned_data['skill'])),
			favorite=re.sub(r'\n|\r','',decode_data(self.cleaned_data['favorite']))
		)

		u.save()

		return u


class UserSchoolForm(forms.Form):
	college = forms.IntegerField(widget=forms.HiddenInput,required=False)
	school = forms.IntegerField(widget=forms.HiddenInput,required=False)
	start_year = forms.IntegerField(widget=forms.HiddenInput,required=False)
	end_year = forms.IntegerField(widget=forms.HiddenInput,required=False)

	def save(self,id):
		u = UserSchool(id=id,college=self.cleaned_data['college'],
			school = self.cleaned_data['school'],
			start_year = self.cleaned_data['start_year'],
			end_year = self.cleaned_data['end_year']
		)

		u.save()

		return u


class PasswordForm(forms.Form):
	oldpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'text'}),error_messages={'required':'旧密码不能为空'})
	newpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'text'}),error_messages={'required':'新密码不能为空'})
	newpasswordagain=forms.CharField(widget=forms.PasswordInput(attrs={'class':'text'}),error_messages={'required':'再次确认你的密码'})

	def verify(self,id):
		try:
			p = UserPassword.objects.get(id=id)
			if p:
				 return p.verify(self.cleaned_data['oldpassword'])
		except ObjectDoesNotExist:
			return ''
		else:
			pass
		finally:
			pass

	def change_password(self,id):
		try:
			p = UserPassword.objects.get(id=id)
			if p:
				p.change_password(self.cleaned_data['newpassword'])
		except ObjectDoesNotExist:
			return ''
		else:
			pass
		finally:
			pass

	def verify_newpassword(self):
		if self.cleaned_data['newpassword']!=self.cleaned_data['newpasswordagain']:
			return False
		else:
			return True

class UserAccountForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'text'}),error_messages={'required':'邮箱不能为空','invalid':'邮箱格式正确'})
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'text'}),error_messages={'required':'密码不能为空'})
	newemail = forms.EmailField(widget=forms.TextInput(attrs={'class':'text'}),error_messages={'required':'新邮箱不能为空','invalid':'邮箱格式不正确'})


	def verify(self,id):
		try:
			errors={}
			p = UserPassword.objects.get(id=id)
			if p:
				 if p.verify(self.cleaned_data['password']):
				 	pass
			 	 else:
			 	 	errors['incorrectpw']='密码不正确'

		 	u = UserEmail.objects.get(id=id)
		 	if u:
		 		if self.cleaned_data['email']==u.email:
		 			pass
	 			else:
	 				errors['incorrectem']='邮箱不正确'

			return errors
		except ObjectDoesNotExist:
			return errors
		else:
			pass
		finally:
			pass

	def change_account(self,id):
		try:
			u = UserEmail.objects.get(id=id)
		 	if u:
		 		u.email = self.cleaned_data['newemail']
		 		u.save()
		except ObjectDoesNotExist:
			raise
		else:
			pass
		finally:
			pass

class UserHeadForm(forms.Form):
	avatarImage = forms.ImageField()



def update_user_avatar(use_id,avatar=None,thumb=None,last_avatar=None):
	if use_id and thumb and avatar and last_avatar:
		User.objects.filter(id=use_id).update(head=thumb,avatar=avatar,last_avatar=last_avatar)


