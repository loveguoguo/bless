from django.contrib.sessions.backends.db import SessionStore as BaseSessionStore

class WeixinSessionStore(BaseSessionStore):
    
    def __init__(self, session_key):
        assert session_key is not None
        super(WeixinSessionStore, self).__init__(session_key)

    def load(self):
        try:
            s = WeixinSession.objects.get(
                session_key=self.session_key,
                expire_date__get=timezone.now()
            )
            return self.decode(s.session_data)
        except (WeixinSession.DoesNotExist, SuspiciousOperation):
            self.create()
            return {}

    def exists(self, session_key):
        return WeixinSession.objects.filter(session_key=session_key).exists()

    def create(self):
        try:
            self.save(must_create=True)
        except CreateError:
            raise RuntimeError('create weixin session error')
        self.modified = True
        self._session_cache = {}
        return 

        
