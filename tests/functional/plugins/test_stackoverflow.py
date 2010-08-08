from eizzek.lib.plugins.stackoverflow import stackoverflow, build_response

from twisted.trial import unittest

class StackoverflowTest(unittest.TestCase):
    
    def test_index(self):
        def assert_questions(response):
            questions = response.split('\n\n')
        
            assert 'Stack Overflow: Top Questions' in response
            assert 51 == len(questions)     # 50 + header
        
        deferred = stackoverflow()
        deferred.addCallback(assert_questions)
        return deferred

    def test_index_limited(self):
        def assert_questions(response):
            questions = response.split('\n\n')
    
            assert 'Stack Overflow: Top Questions' in response
            assert 11 == len(questions)
            
        deferred = stackoverflow(limit=10)
        deferred.addCallback(assert_questions)
        return deferred
    
    def test_tagged(self):
        def assert_questions(response):
            questions = response.split('\n\n')
        
            assert 'Stack Overflow: python tag' in response
        
        deferred = stackoverflow(tag='python')
        deferred.addCallback(assert_questions)
        return deferred
    
    def test_tagged_limited(self):
        def assert_questions(response):
            questions = response.split('\n\n')
        
            assert 'Stack Overflow: python tag' in response
            assert 4 == len(questions)
        
        deferred = stackoverflow(tag='python', limit=3)
        deferred.addCallback(assert_questions)
        return deferred