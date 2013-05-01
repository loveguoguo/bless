from django.db import models
from django.utils.translation import ugettext_lazy as _


class WeixinSessionManager(models.Manager):
    def encode(self, session_dict):
        """
        Returns the given session dictionary pickled and encoded as a string.
        """
        return SessionStore().encode(session_dict)

    def save(self, session_key, session_dict, expire_date):
        s = self.model(session_key, self.encode(session_dict), expire_date)
        if session_dict:
            s.save()
        else:
            s.delete() # Clear sessions with no data.
        return s


class WeixinSession(models.Model):
    """copy from django contrib sessions"""
    session_key = models.CharField(_('session key'), max_length=40,
                                   primary_key=True)
    session_data = models.TextField(_('session data'))
    expire_date = models.DateTimeField(_('expire date'), db_index=True)
    objects = WeixinSessionManager()

    class Meta:
        db_table = 'django_weixin_session'
        verbose_name = _('weixin_session')
        verbose_name_plural = _('weixin_sessions')

    def get_decoded(self):
        return SessionStore().decode(self.session_data)


# At bottom to avoid circular import
from backends.db import WeixinSessionStore as SessionStore
