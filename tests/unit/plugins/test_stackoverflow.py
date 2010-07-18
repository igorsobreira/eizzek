import os.path
import unittest

from eizzek.lib.plugins.stackoverflow import build_response, QuestionsParser, TaggedQuestionsParser

here = os.path.realpath(os.path.dirname(__file__))
python_tag_page = os.path.join(here, 'stackoverflow_python_tag.html')
index_page = os.path.join(here, 'stackoverflow_top_questions.html')

class ParseTestCase(unittest.TestCase):

    def setUp(self):
        with open(index_page) as file_obj:
            self.index_data = QuestionsParser().parse( file_obj.read() )
        
        with open(python_tag_page) as file_obj:
            self.tagged_data = TaggedQuestionsParser().parse( file_obj.read() )
    
    def test_read_all_elements(self):
        assert 50 == len(self.tagged_data)
        assert 96 == len(self.index_data)
    
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
    

