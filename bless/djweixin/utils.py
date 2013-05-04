#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings
import simplejson
import xml.etree.ElementTree as ET
import hashlib
import time

def checkSignature(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echoStr = request.GET.get('echostr')
    
    tmplist = [settings.WEIXIN_TOKEN, timestamp, nonce]
    tmplist.sort()
    tmpstr = '%s%s%s'%tuple(tmplist)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr)
    else:
        raise Http404


class HandlerBase(object):
    DefaultReply = ''
    def __init__(self, msg):
        self.msg = msg

    def __call__(self):
        pass

class ReplyBase(object):
    def __init__(self, msg, info):
        self.touser = msg['FromUserName']
        self.fromuser = msg['ToUserName']
        self.content = info

class TextReply(ReplyBase):
    '''文本消息'''
    extTpl = ('<xml>'
            '<ToUserName><![CDATA[%s]]></ToUserName>'
            '<FromUserName><![CDATA[%s]]></FromUserName>'
            '<CreateTime>%s</CreateTime>'
            '<MsgType><![CDATA[text]]></MsgType>'
            '<Content><![CDATA[%s]]></Content>'
            '<FuncFlag>0</FuncFlag>'
            '</xml>')

    def genReply(self):
        return self.extTpl%(self.touser, self.fromuser, str(int(time.time())), self.content) 
        

class MusicReply(ReplyBase):
    '''语音消息'''
    extTpl =( '<xml'
                '<ToUserName><![CDATA[%s]]></ToUserName>'
                '<FromUserName><![CDATA[%s]]></FromUserName>'
                '<CreateTime>%s</CreateTime>'
                '<MsgType><![CDATA[music]]></MsgType>'
                '<Music>'
                    '<title><![CDATA[%s]]></Title>'
                    '<Description><![CDATA[%s]]></Description>'
                    '<MusicUrl><![CDATA[%s]]></MusicUrl>'
                    '<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>'
                '</Music>'
                '<FuncFlag>0</FuncFlag>'
            '</xml>')

    def genReply(self):
        title = self.content.get('title', '')
        description = self.content.get('description', '')
        musicurl = self.content.get('musicurl', '')
        hqmusicurl = self.content.get('hqmusicurl', '')
        
        reply = self.extTpl%(self.touser, self.fromuser, str(int(time.time())),
                            title, description, musicurl, hqmusicurl)
        return reply


class NewsReply(ReplyBase):
    '''图文消息'''
    extTpl = ('<xml>'
                '<ToUserName><![CDATA[%s]]></ToUserName>'
                '<FromUserName><![CDATA[%s]]></FromUserName>'
                '<CreateTime>%s</CreateTime>'
                '<MsgType><![CDATA[news]]></MsgType>'
                '<ArticleCount>%s</ArticleCount>'
                '<Articles>%s</Articles>'
                '<FuncFlag>0</FuncFlag>'
            '</xml>')
    itemTpl = ('<item>'
                '<Title><![CDATA[%s]]></Title>'
                '<Description><![CDATA[%s]]></Description>'
                '<PicUrl><![CDATA[%s]]></PicUrl>'
                '<Url><![CDATA[%s]]></Url>'
              '</item>')

    def genReply(self):
        count = len(self.content)
        itemMsg_list = []
        for item in self.content:
            itemMsg = self.itemTpl%(item['title'], item['description'], item['picurl'], item['url'])
            itemMsg_list.append(itemMsg)
        reply = self.extTpl%(self.touser, self.fromuser, str(int(time.time())), len(itemMsg_list),
                            ''.join(itemMsg_list))
        return reply
    

class WeiXin(object):
    msgtype_dict =  {
        'text':HandlerBase, 
        'image': HandlerBase, 
        'event': HandlerBase,
        'location': HandlerBase,
        'link': HandlerBase,
        }
    replytype_dict = {
        'text': TextReply,
        'music': MusicReply,
        'news': NewsReply, 
    }
    def __init__(self, request):
        if hasattr(request, 'weixindata'):
            self.msg = request.weixindata
        else:
            rootElem = ET.fromstring(request.raw_post_data)
            self.msg = self.parseMsgXml(rootElem)
        self.weixinsession = request.weixinsession
        self.handler = self.msgtype_dict[self.msg['MsgType']](self.msg) 
    
    @classmethod
    def register_handler(cls, key, handler):
        if key not in cls.msgtype_dict:
            raise Exception('weixin not have %s msg type'%key)
        cls.msgtype_dict[key] = handler
 
    @classmethod             
    def parseMsgXml(cls, rootElem):
        msg = {}
        if rootElem.tag == 'xml':
            for child in rootElem:
                msg[child.tag] = smart_str(child.text)
        return msg

    def genReply(self, request=None):
        data = self.handler(request)
        replytype = data.get('type', 'text')
        reply_handler = self.replytype_dict.get(replytype)
        replyer = reply_handler(self.msg, data['info'])
        reply = replyer.genReply()
        return reply
