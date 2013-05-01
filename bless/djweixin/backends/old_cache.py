#!/usr/bin/env python
#-*- coding:utf8 -*-
from django.contrib.sessions.backends.base import CreateError
from django.contrib.sessions.backends.cache import SessionStore as BaseSessionStore

KEY_PREFIX = "django.weixin.sessions.cache"

class WeixinSessionStore(BaseSessionStore):
   
    @property
    def cache_key(self):
        return KEY_PREFIX + self._get_or_create_session_key()
    
    def create(self):
        try:
            self.save(must_create=True)
        except CreateError:
            raise RuntimeError(
                "Unable to create a new weixin session key."
                "It is likely that the cache is unavailable.")

        self.modified = True
        return 

    def exists(self, session_key):
        return (KEY_PREFIX + session_key) in self._cache

    def delete(self, session_key=None):
        if session_key is None:
                if self.session_key is None:
                    return
                session_key = self.session_key
        self._cache.delete(KEY_PREFIX + session_key)
