from redis import Redis

class SessionPersistence(object):

    def __init__(self):
        self._redis = None
        self.host = 'localhost'
        self.port = 6379

    def begin(self, jid, plugin_name):
        if self.is_open(jid):
            raise IOError(u"This JID already has an open session")
        self.redis.hset(jid, 'plugin', plugin_name)

    def end(self, jid):
        self.redis.hdel(jid, 'plugin')
    
    def is_open(self, jid):
        return self.redis.hlen(jid) > 0

    @property
    def redis(self):
        if not self._redis:
            self._redis = Redis(host=self.host, port=self.port)
        return self._redis

session = SessionPersistence()
