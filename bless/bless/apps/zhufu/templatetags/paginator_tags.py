#!/usr/bin/env python
# -*- coding:utf8 -*-
from django import template
from django.utils.html import conditional_escape

register = template.Library()

@register.inclusion_tag('tag_template/paginator.html')
def simple_paginator(items, url, key='tag', values=[], pre_num=3, after_num=4):
    if items.number >= pre_num:
        page_list = items.paginator.page_range[items.number-pre_num:items.number+after_num]
    else:
        page_list = items.paginator.page_range[0:items.number+after_num]
    if '?' not in url:
        url = url + '?'
    if values:
        if not isinstance(values, list):
            values = [values]
        url = url + '&'.join(['%s=%s'%(key, i) for i in values])
    data = {
        'url': url,
        'number': items.number,
        'previous_page_number': items.has_previous() and items.previous_page_number or None,
        'page_list': page_list,
        'next_page_number': items.has_next() and items.next_page_number or None,
        'num_pages': items.paginator.num_pages,
    } 
    return data 


@register.inclusion_tag('tag_template/paginator.html')
def dict_paginator(items, url , key='search_words', values=[], pre_num=3, after_num=4):
    start_number = max(items['number'] - pre_num, 1)
    end_number = min(items['number'] + after_num, items['paginator']['num_pages'])
    page_list = range(start_number, end_number + 1)
    if '?' not in url:
        url = url + '?'
    if values:
        if not isinstance(values, list):
            values = [values]
        url = url + '&'.join(['%s=%s'%(key, i) for i in values])
    data = { 
        'url': url,
        'number': items['number'],
        'previous_page_number': items['number'] > 1 and items['previous_page_number'] or None,
        'page_list': page_list,
        'next_page_number': items['number'] < items['paginator']['num_pages'] and items['next_page_number'] or None,
        'num_pages': items['paginator']['num_pages'],
    } 
    return data 
  
