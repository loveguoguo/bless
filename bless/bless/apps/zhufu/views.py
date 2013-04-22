#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.loader import get_template
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from models import *
from taggit.models import Tag, TaggedItem
import simplejson
from indexes import Search

SEARCH = Search(settings.INDEX_ROOT)

def common_paginator(request, article_list):
    paginator = Paginator(article_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return articles
    
def get_article_tags(articles, tagid=None):
    article_ids = [i.id for i in articles]
    ct = ContentType.objects.get_for_model(Article)
    tagged_items = TaggedItem.objects.filter(content_type=ct, object_id__in=article_ids)
    article_tags = {}
    tagids = [i.tag_id for i in tagged_items]
    tags = Tag.objects.filter(id__in=tagids)
    tags_dict = dict([(t.id, t) for t in tags])
    for i in tagged_items:
        article_tags.setdefault(i.object_id, []).append(tags_dict[i.tag_id])
    return article_tags, tagid and tags_dict.get(tagid)

@require_GET
def home(request):
    '''首页'''
    article_list = Article.objects.all()
    articles = common_paginator(request, article_list)
    article_tags, tag = get_article_tags(articles) 
    tags = Tag.objects.all()
    data = {
        'articles': articles,
        'article_tags': article_tags,
        'request': request,
        'tags': tags,
        'page': 'home',
    }
    return render_to_response('zhufu/home.html', data)

@require_GET
def tag_articles(request, tagid, page='home'):
    article_list = Article.objects.filter(tags__id=tagid)
    articles = common_paginator(request, article_list)
    article_tags, tag = get_article_tags(articles, int(tagid)) 
    tags = Tag.objects.all()
    tags_dict = dict([(t.id, t) for t in tags])

    data = {
        'articles': articles,
        'request': request,
        'tags': tags,
        'tag': tag,
        'article_tags': article_tags,
        'page': page,
    }
    return render_to_response('zhufu/home.html', data)
 
@require_GET
def festival(request):
    '''节日'''
    #tag = Tag.objects.get(name='节日')
    article_list = Article.objects.filter(tags__name__in=['节日'])
    articles = common_paginator(request, article_list)
    article_tags, tag = get_article_tags(articles) 
    tags = Tag.objects.all()
    data = {
        'articles': articles,
        'article_tags': article_tags,
        'request': request,
        'tags': tags,
        'page': 'festival',
    }
    return render_to_response('zhufu/home.html', data)

@require_GET
def birthday(request):
    '''生日'''
    article_list = Article.objects.filter(tags__name__in=['生日'])
    articles = common_paginator(request, article_list)
    article_tags, tag = get_article_tags(articles) 
    tags = Tag.objects.all()
    data = {
        'articles': articles,
        'article_tags': article_tags,
        'request': request,
        'tags': tags,
        'page': 'birthday',
    }
    return render_to_response('zhufu/home.html', data)

@require_GET
def others(request):
    '''其他'''
    article_list = Article.objects.exclude(tags__name__in=['生日', '节日'])
    articles = common_paginator(request, article_list)
    article_tags, tag = get_article_tags(articles) 
    tags = Tag.objects.all()
    data = {
        'articles': articles,
        'article_tags': article_tags,
        'request': request,
        'tags': tags,
        'page': 'others',
    }
    return render_to_response('zhufu/home.html', data)
        
@require_GET
def search(request):
    '''搜索,其实是根据tag匹配,不是根据内容'''
    words = request.REQUEST.get('words')
    if not words:
        return HttpResponseRedirect('/')
    
    questions = SEARCH.search_by_page(words, 1)
    qids = [i['id'] for i in questions['object_list']]
    article_list = Article.objects.filter(questions__id__in=qids).distinct()
    articles = common_paginator(request, article_list)
    articles = sorted(articles, key=lambda x:qids.index(x))
    article_tags, tag = get_article_tags(articles) 
    tags = Tag.objects.all()
    data = {
        'articles': articles,
        'article_tags': article_tags,
        'request': request,
        'tags': tags,
        'words': words,
        'page': 'search',
    }
    return render_to_response('zhufu/home.html', data)

