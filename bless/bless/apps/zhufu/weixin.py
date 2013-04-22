#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings
from models import *
from taggit.models import Tag, TaggedItem
import simplejson
from indexes import Search
import xml.etree.ElementTree as ET
import hashlib
import time

SEARCH = Search(settings.INDEX_ROOT)
TOKEN = 'token'
DEFAULTREPLY = '不知道哦,你換個方式問問?'

@csrf_exempt
def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET')
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404

def checkSignature(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echoStr = request.GET.get('echostr')
    
    tmplist = [TOKEN, timestamp, nonce]
    tmplist.sort()
    tmpstr = '%s%s%s'%tuple(tmplist)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr)
    else:
        raise Http404

def parseMsgXml(rootElem):
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg

def genReplyXml(msg, replyContent):
    extTpl = '<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>';
    extTpl = extTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),
                        'text', replyContent)
    return extTpl

def responseMsg(request):
    rawStr = smart_str(request.raw_post_data)
    msg = parseMsgXml(ET.fromstring(rawStr))
    queryStr = msg.get('Content')
    if not queryStr:
        replyContent = DEFAULTREPLY
    else:
        questions = SEARCH.search_by_page(queryStr, 1, 1)
        qids = [i['id'] for i in questions['object_list']]
        article_list = Article.objects.filter(questions__id__in=qids).distinct()
        if not article_list:
            replyContent = DEFAULTREPLY
        else:
            article = article_list[0]
            if article.imgurl:
                replyContent = '%s\n%s'%(article.content, article.imgurl)
            else:
                replyContent = article.content
    data = genReplyXml(msg, replyContent)
    return HttpResponse(data)

