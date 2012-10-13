# -*- coding: utf-8 -*- 
from auth.models import UserPassword,UserEmail
from models import *
from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.core.exceptions import ObjectDoesNotExist

class CustomeRadioRenderer(forms.widgets.RadioFieldRenderer):
	def render(self):
		"""Outputs a <ul> for this set of radio fields."""
		return mark_safe(u'\n%s\n' % u'\n'.join([u'%s'% force_unicode(w) for w in self]))






