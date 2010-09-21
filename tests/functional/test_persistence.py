from unittest import TestCase
from redis import Redis

from eizzek.lib.persistence import SessionPersistence

class PersistenceTest(TestCase):
    
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self._redis = Redis(host='localhost', port=6379)    # db ? 
        self.session = SessionPersistence()

    def setUp(self):
        self.jid = 'igor@igorsobreira.com/Adium1234'
        self._redis.hdel(self.jid, 'plugin')

    def test_begin_creates_hash(self):
        assert not self._redis.hget(self.jid, 'plugin')
        
        self.session.begin(self.jid, 'translate')

        assert 'translate' == self._redis.hget(self.jid, 'plugin')

    def test_duplicates_begins_raises_ioerror(self):
        self.session.begin(self.jid, 'translate')
        try:
            self.session.begin(self.jid, 'translate')
            assert 0, u"Should raise IOError"
        except IOError:
            pass

    def test_end_removes_hash(self):
        self.session.begin(self.jid, 'translate')

        assert self._redis.hget(self.jid, 'plugin')
        
        self.session.end(self.jid)
        
        assert not self._redis.hget(self.jid, 'plugin')
    
    def test_is_open_method(self):
        assert not self.session.is_open(self.jid)

        self._redis.hset(self.jid, 'plugin', 'translate')

        assert self.session.is_open(self.jid)

