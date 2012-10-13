# -*- coding: utf-8 -*- 


"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import unittest
from models import *


class TestAuth(unittest.TestCase):
	def setUp(self):
		self.email='zhyq0826@126.com'
		self.password='123456'
		self.nickname='三月沙'

	def testAuth(self):
		email = self.email

		reset_password(5,'124')

		







		







