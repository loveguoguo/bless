#!/usr/bin/env python
#-*- coding:utf8-*-
import os
import sys
import django.core.handlers.wsgi

#project_path = '/home/project/qinxi/'
#project_path = os.path.abspath(os.path.dirname(__file__))
#site_path = '/home/project/'
#sys.path.append(site_path)
#sys.path.append(project_path)
sys.path.append(__file__[:__file__.rfind('/')])
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'
application = django.core.handlers.wsgi.WSGIHandler()
