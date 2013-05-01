from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sessions.models import SessionManager, Session

class WeixinSessionManager(SessionManager):pass

class WeixinSession(Session):
    class Meta:
        db_table = 'django_weixin_session'
        verbose_name = _('weixin_session')
        verbose_name_plural = _('weixin_sessions')
