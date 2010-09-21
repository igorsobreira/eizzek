from redis import Redis
from eizzek import config

class SessionPersistence(object):

    def __init__(self):
        self._redis_client = None
        self.host = config.REDIS_HOST
        self.port = config.REDIS_PORT
        self.db = config.REDIS_DB

    def begin(self, jid, plugin_name):
        if self.is_open(jid):
            raise IOError(u"This JID already has an open session")
        self._redis.hset(jid, 'plugin', plugin_name)

    def end(self, jid):
        self._redis.hdel(jid, 'plugin')
    
    def is_open(self, jid):
        return self._redis.hlen(jid) > 0
    
    def get_current(self, jid):
        return self._redis.hgetall(jid)

    @property
    def _redis(self):
        if not self._redis_client:
            self._redis_client = Redis(host=self.host, port=self.port, db=self.db)
        return self._redis_client

session = SessionPersistence()
