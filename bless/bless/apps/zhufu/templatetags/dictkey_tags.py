
#!/usr/bin/env python
# -*- coding:utf8 -*-
from django import template

register = template.Library()

def key(d, keyname, defaultvalue=None):
    try:
        value = d[keyname]
    except KeyError:
        value = defaultvalue
    return value

register.filter('key', key)
