import os
import sys

path='/var/www'
if path not in sys.path:
    sys.path.insert(0,'/var/www')

sys.path.append('var/www/linkusall')

os.environ['DJANGO_SETTINGS_MODULE'] = 'linkusall.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
