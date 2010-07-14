import os.path
import unittest

from eizzek.lib.plugins.stackoverflow import parse

here = os.path.realpath(os.path.dirname(__file__))
python_tag_page = os.path.join(here, 'stackoverflow_python_tag.html')

class ParseTestCase(unittest.TestCase):

    def setUp(self):
        with open(python_tag_page) as file_obj:
            self.data = parse(file_obj.read())
    
    def test_read_all_elements(self):
        assert 50 == len(self.data)
    
    def test_question_attributes(self):
        question = self.data[0]
        
        assert question['summary'] == u'Python Rpy R data processing optimization'
        assert question['link'] == u'http://stackoverflow.com/questions/3242670/python-rpy-r-data-processing-optimization'
        assert [u'python', u'r', u'rpy2'] == question['tags']
        assert '0' == question['votes']
        assert '0' == question['answers']
        assert '0' == question['views']