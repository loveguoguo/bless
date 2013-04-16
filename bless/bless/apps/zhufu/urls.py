#!/usr/bin/env python
#-*- coding:utf8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from bless.apps.zhufu import views, weixin

urlpatterns = patterns('bless.apps.zhufu.views',
    url(r'^/?$', 'home', name='zhufu_home'), 
    url(r'^tag/(?P<tagid>\d+)/?$', 'tag_articles', name='tag_articles'),
    url(r'^festival/?$', 'festival', name='festival_articles'),
    url(r'^birthday/?$', 'birthday', name='birthday_articles'),
    url(r'^others/?$', 'others', name='others_articles'),
    url(r'^search/?$', 'search', name='search'),
)

urlpatterns += patterns('bless.apps.zhufu.weixin',
    url(r'^weixin/$', 'method_splitter', {'GET': weixin.checkSignature,
                                        'POST': weixin.responseMsg}),
)
