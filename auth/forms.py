# -*- coding: utf-8 -*- 

from django import forms

class RegisterForm(forms.Form):
	email = forms.EmailField(widget = forms.TextInput(attrs = {'class':'text required'}),error_messages={"required":"Email不能为空","invalid":"Email格式不正确"})
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password required'}),error_messages={"required":"密码不能为空"})
	nickname = forms.CharField(widget = forms.TextInput(attrs = {'class':'text required'}),error_messages={"required":"昵称不能为空"})
	role = forms.CharField(widget=forms.HiddenInput,required=False)


class ResetPasswordApplyForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'text'}),error_messages={"required":"Email不能为空","invalid":"Email格式不正确"})


class ResetPasswordForm(forms.Form):
	"""docstring for ResetPasswordForm"""
	newpassword = forms.CharField(widget=forms.PasswordInput,error_messages={"required":"密码不能为空"})
	newpasswordagain = forms.CharField(widget=forms.PasswordInput,error_messages={"required":"密码不能为空"})
		

class LoginForm(forms.Form):
	email = forms.EmailField(widget = forms.TextInput(attrs = {'class':'text required'}),error_messages={"required":"Email不能为空","invalid":"Email格式不正确"})
	password = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'password required'}),error_messages={"required":"密码不能为空"})
	remember = forms.CharField(widget=forms.CheckboxInput,required=False)
	