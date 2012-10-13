# -*- coding: utf-8 -*- 
# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext,Template, Context
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
from models import *
from forms import *
import re
import os,ImageFile,uuid
from django.conf import settings

from django.http import Http404,HttpResponse
from django.template import TemplateDoesNotExist
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from linkusall.util import Paginator,EmptyPage,random_char
from linkusall.subject.models import get_subjects,get_c_tags,get_c_subjects,get_one_subject

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 


@csrf_exempt
def uploadimage(request):
	try:
		u = request.session['user']
		user_id=u.id
		if request.method=='POST':
			form = ImageUploadForm(request.POST,request.FILES)
			if form.is_valid():
				path_file,size,status =  handle_upload_image(request.FILES['imagefileupload'],user_id)
				width,height = size
				if status:
					t = Template("{status:true,imgurl:'"+path_file+"',width:"+str(width)+",height:"+str(height)+"}")
					html = t.render(Context()) 
					return HttpResponse(html)
				else:
				    t = Template("{status:false,error:'上传失败'}")
				    html = t.render(Context()) 
				    return HttpResponse(html)
			else:
				t = Template("{status:false,error:'上传失败'}")
				html = t.render(Context()) 
				return HttpResponse(html)
			return HttpResponse()
		else:
			raise Http404()
	except Exception, e:
		raise 

def handle_upload_image(imagefile,id=None):
	if imagefile:
		now = datetime.now()
		t = "%d%d%d%d%d"%(now.year,now.month,now.day,now.minute,now.second)
		img=None
		path=os.path.join(settings.MEDIA_ROOT,'blog')
		file_name=t+"-"+str(id)+".jpg"
		path_file=os.path.join(path,file_name)
		parser=ImageFile.Parser()
		if imagefile.multiple_chunks():
			for chunk in imagefile.chunks():
				parser.feed(chunk)
			img = parser.close()
		else:
			parser.feed(imagefile.read())
			img = parser.close()

		size = img.size

		try:
			if img.mode!="RGB":
				img = img.convert("RGB")
			img.save(path_file,'jpeg',quality=100)
		except Exception, e:
			return file_name,size,False
			
		return file_name,size,True

	return None,False
	

    