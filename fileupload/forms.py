# -*- coding: utf-8 -*- 

from django import forms
from models import *
from datetime import datetime
import re
from linkusall.util import decode_data
from linkusall.subject.models import Tag,Subject,process_tags_subjects
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class ImageUploadForm(forms.Form):
	imagefileupload = forms.ImageField()
