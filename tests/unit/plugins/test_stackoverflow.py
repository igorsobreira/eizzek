import os.path
import unittest

from eizzek.plugins.stackoverflow import build_response, QuestionsParser, TaggedQuestionsParser
from eizzek import registry, PluginResolver

class RegexTestCase(unittest.TestCase):
    
    def setUp(self):
        # unregister the original plugin
        self.stackoverflow_regex, self.stackoverflow_function = registry.plugins['stackoverflow']
        registry.unregister('stackoverflow')
        
        # register a mock, just to verify if the regex is working
        self.called = False
        self.tag = None
        self.limit = 50
        
        def stackoverflow_mock(conn, limit=None, tag=None, **kw):
            self.called = True
            self.tag = tag
            self.limit = int(limit) if limit else 50
        
        registry.register('stackoverflow', self.stackoverflow_regex, stackoverflow_mock)
        
        self.resolver = PluginResolver()

    def tearDown(self):
        # undo de mock
        registry.unregister('stackoverflow')
        registry.register('stackoverflow', self.stackoverflow_regex, self.stackoverflow_function)
    
    def test_simple(self):
        self.resolver.resolve('stackoverflow', {})
        
        assert self.called
        assert self.tag is None
        assert 50 == self.limit
    
    def test_tagged(self):
        self.resolver.resolve('stackoverflow python', {})
        
        assert self.called
        assert 'python' == self.tag
        assert 50 == self.limit
        
    def test_limit(self):
        self.resolver.resolve('stackoverflow 10', {})
        
        assert self.called
        assert self.tag is None
        assert 10 == self.limit
    
    def test_tagged_limit(self):
        self.resolver.resolve('stackoverflow 15 python', {})
        
        assert self.called
        assert 'python' == self.tag
        assert 15 == self.limit
    
    def test_different_tags(self):
        tags = ('c++', 'c#', 'regular-language', 'asp.net', '.net', 'actionscript-3')
        
        for tag in tags:
            self.resolver.resolve('stackoverflow ' + tag, {})
            
            assert self.called
            assert tag == self.tag
            
            self.called, self.tag = False, None
    


class ParseTestCase(unittest.TestCase):

    here = os.path.realpath(os.path.dirname(__file__))
    python_tag_page = os.path.join(here, 'stackoverflow_python_tag.html')
    index_page = os.path.join(here, 'stackoverflow_top_questions.html')

    def setUp(self):
        with open(self.index_page) as file_obj:
            self.index_data = QuestionsParser().parse( file_obj.read() )
        
        with open(self.python_tag_page) as file_obj:
            self.tagged_data = TaggedQuestionsParser().parse( file_obj.read() )
    
    def test_read_all_elements(self):
        assert 50 == len(self.tagged_data)
        assert 96 == len(self.index_data)
    
    def test_read_limited_elements(self):
        parser = QuestionsParser()
        with open(self.index_page) as file_obj:
            data = parser.parse( file_obj.read(), limit=10 )
        
        assert 10 == len(data)
    
    def test_tagged_question_attributes(self):
        question = self.tagged_data[0]
        
        assert u'Python Rpy R data processing optimization' == question['summary']
        assert u'http://stackoverflow.com/questions/3242670/python-rpy-r-data-processing-optimization' == question['link'] 
        assert [u'python', u'r', u'rpy2'] == question['tags']
        assert '0' == question['votes']
        assert '0' == question['answers']
        assert '0' == question['views']
    
    def test_index_question_attributes(self):
        question = self.index_data[0]
        
        assert u'How to multiply two big big numbers' == question['summary']
        assert u'http://stackoverflow.com/questions/3275986/how-to-multiply-two-big-big-numbers' == question['link']
        assert [u'java', u'arrays', u'homework', u'problem', u'multiplication'] == question['tags']
        assert '6' == question['votes']
        assert '7' == question['answers']
        assert '251' == question['views']
    

class BuildResponseTestCase(unittest.TestCase):
    
    def setUp(self):    
        self.questions = [
            {
                'summary': 'Is it possible to mix generator and a recursive function ?',
                'link': 'http://stackoverflow.com/questions/3276956/pyhon-is-it-possible-to-mix-generator-and-a-recursive-function',
                'tags': ['python','recursive'],
                'votes': '1',
                'answers': '3',
                'views': '20',
            },
            {
                'summary': 'Set Django ModelForm visible fields at runtime?',
                'link': 'http://stackoverflow.com/questions/3276896/set-django-modelform-visible-fields-at-runtime',
                'tags': ['python','django'],
                'votes': '4',
                'answers': '2',
                'views': '10',
            },
        ]
    
    def test_no_tag(self):
        response = build_response(self.questions)
        data = response.split('\n\n')
        
        assert 3 == len(data)
        
        header, question1, question2 = data
    
        assert u'Stack Overflow: Top Questions' == header
    
        line1, line2, line3 = question1.split('\n')
    
        assert 'Is it possible to mix generator and a recursive function ?' == line1
        assert 'http://stackoverflow.com/questions/3276956/pyhon-is-it-possible-to-mix-generator-and-a-recursive-function' == line2
        assert 'Tags: python, recursive.   (votes: 1, answers: 3, views: 20)' == line3
    
        line1, line2, line3 = question2.split('\n')
    
        assert 'Set Django ModelForm visible fields at runtime?' == line1
        assert 'http://stackoverflow.com/questions/3276896/set-django-modelform-visible-fields-at-runtime' == line2
        assert 'Tags: python, django.   (votes: 4, answers: 2, views: 10)' == line3

    def test_tagged(self):
        response = build_response(self.questions, tag='recursive')
        data = response.split('\n\n')
        
        assert 2 == len(data)
        assert u'Stack Overflow: recursive tag' == data[0]
    

