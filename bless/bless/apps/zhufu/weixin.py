#!/usr/bin/env python
#-*- coding:utf8 -*-

from urlparse import urljoin
import re

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from models import *
from taggit.models import Tag, TaggedItem
from djweixin.utils import checkSignature, HandlerBase, WeiXin
from indexes import Search

SEARCH = Search(settings.INDEX_ROOT)

IP_REGEX = re.compile(r'^(\d+[.]){3,3}\d+(:\d+)?$')

@csrf_exempt
def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET')
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404

class TextHandler(HandlerBase):
    DefaultReply = '没找到符合要求的祝福，请换个条件'
    NumPerPage = 3

    def more(self, request):
        '''获取上一次查询的更多内容'''
        last_qid = request.weixinsession.get('last_qid')
        last_page = request.weixinsession.get('last_page', 0)
        if not last_qid:
            return self.DefaultReply
        article_list = Article.objects.filter(questions__id=last_qid)
        paginator = Paginator(article_list, self.NumPerPage)
        try:
            articles = paginator.page(last_page + 1)
        except EmptyPage:
            if last_page:
                return '没有更多内容啦，欢迎查询其他祝福语'
            else:
                return '不好意思，没有查到相关的祝福语，请输入其他条件进行查询'
        request.weixinsession['last_page'] = last_page + 1
        return articles

    def _get(self, request, index):
        '''获取指定序号的祝福语'''
        last_qid = request.weixinsession.get('last_qid')
        if not last_qid:
            return self.DefaultReply
        article_list = Article.objects.filter(questions__id=last_qid)
        try:
            article = article_list[index]
        except IndexError:
            return '没有该序号的祝福语'
        return article.content.encode('utf8')

    def __call__(self, request):
        queryStr = self.msg.get('Content')
        if not queryStr:
            replyContent = self.DefaultReply
        else:
            if queryStr == '游戏':
                host = request.get_host()
                if IP_REGEX.match(host):
                    host = 'http://%s'%host 
                articles = '微信小游戏：另类打飞机,请猛戳<a href="%s/static/fireplane/index.html">这里</a>' % host
            elif queryStr.isdigit():
                articles = self._get(request, int(queryStr))
            else:
                if queryStr.lower() != 'm':
                    questions = SEARCH.search_by_page(queryStr, 1, 1)
                    qids = [i['id'] for i in questions['object_list']]
                    request.weixinsession['last_querystr'] = queryStr
                    request.weixinsession['last_qid'] = qids and qids[0] or None
                    request.weixinsession['last_page'] = 0
                articles = self.more(request)    
            if isinstance(articles, str):
                return {'type':'text', 'info': articles}
            else:
                _type = 'text'
                for article in articles:
                    if article.imgurl:
                        _type = 'news'
                        break
                if _type == 'text':
                    article_sep = '\n\n'
                    startindex = (request.weixinsession['last_page'] - 1) * self.NumPerPage
                    content = article_sep.join(['%s:\n%s'%(startindex+i, articles[i].content.encode('utf8'))\
                                                     for i in range(len(articles))])
                    while len(content) >= 2000 and article_sep in content:
                        content = content[:content.rfind(article_sep)]
                    content = '%s%s输入m可以查看更多\n输入每条祝福语前面的序号，会单独发送该条祝福语'%(content, article_sep)
                else:
                    items = []
                    host = request.get_host()
                    if IP_REGEX.match(host):
                        host = 'http://%s'%host 
                    for article in articles:
                        item = {
                                'title': article.content[:10].encode('utf8'), 
                                'description': article.content.encode('utf8'),
                                'picurl': urljoin(host, article.imgurl.url),
                                'url': urljoin(host, 
                                            '%s?words=%s'%(reverse('search'), request.weixinsession['last_querystr'])),
                            }
                        items.append(item)
                    content = items
                return {'type':_type, 'info':content}
                

class EventHandler(HandlerBase):
    welcome = '感谢关注节日生日祝福语,你可以输入条件查询祝福语'
    def __call__(self, request):
        event = request.weixindata.get('Event')
        if event.lower() == 'subscribe':
            return {'type':'text', 'info': self.welcome}

class ImageHandler(HandlerBase):
    pass

class LocationHandler(HandlerBase):
    pass

class LinkHandler(HandlerBase):
    pass

WeiXin.register_handler('text', TextHandler)
WeiXin.register_handler('event', EventHandler)


def responseMsg(request):
    weixin = WeiXin(request)
    data = weixin.genReply(request)
    return HttpResponse(data)

