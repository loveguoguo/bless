#!/usr/bin/env python
#-*- coding:utf8 -*-
import time
import xml.etree.ElementTree as ET
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module
from django.utils.encoding import smart_str, smart_unicode

class WeixinSessionMiddleware(object):
    def process_request(self, request):
        if request.path != settings.WEIXIN_URL or request.method != 'POST':
            return
        try:
            rawStr = smart_str(request.raw_post_data)
            rootElem = ET.fromstring(rawStr)
            msg = {}
            if rootElem.tag == 'xml':
                for child in rootElem:
                    msg[child.tag] = smart_str(child.text)
            request.weixindata = msg 
            engine = import_module(settings.WEIXIN_SESSION_ENGINE)
            request.weixinsession = engine.WeixinSessionStore(msg['FromUserName']) 
        except:
            import traceback
            traceback.print_exc()
            raise Http404

    def process_response(self, request, response):
        if request.path != settings.WEIXIN_URL:
            return response
        try:
            modified = request.weixinsession.modified
        except AttributeError:
            pass
        else:
            if modified and response.status_code != 500:
                request.weixinsession.save()
        return response
