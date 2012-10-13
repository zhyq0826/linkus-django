# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext,Template, Context
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
from models import *
import re

from django.http import Http404,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError

from linkusall.util import Paginator,EmptyPage,decode_data

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 


def query_tag(request):
	
	q = request.GET.get('q')
	q = decode_data(q)
	result = search_tags(q)

	return HttpResponse(result, mimetype="text/json")


