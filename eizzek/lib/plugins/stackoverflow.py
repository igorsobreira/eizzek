from lxml import html as lhtml
from urllib import urlopen

from eizzek.lib.decorators import plugin


URL = 'http://stackoverflow.com/'
TAG_URL = 'http://stackoverflow.com/questions/tagged/%s'

@plugin(r'^stackoverflow ?(?P<limit>\d+)? ?(?P<tag>[a-zA-Z0-9\+\#\-\.]+)?$')
def stackoverflow(limit=None, tag=None):
    '''
    Stack Overflow plugin, get questions from http://stackoverflow.com/
    
    Usage:
    
        stackoverflow
            # returns the latest questions
        
        stackoverflow 10
            # returns the latest 10 questions
        
        stackoverflow python
            # returns the latest questions of tag "python"
        
        stackoverflow python 15
            # returns the latest 15 questions of tag "python"
        
    If no limit parameter is passed, default is 50
    
    '''
    limit = int(limit) if limit else 50
    if tag:
        url = TAG_URL % tag
        parser = TaggedQuestionsParser()
    else:
        url = URL
        parser = QuestionsParser()
    
    page = urlopen(url).read()
    questions = parser.parse(page, limit)
    
    return build_response(questions, tag)


def build_response(questions, tag=None):
    response = u'Stack Overflow: '
    if tag:
        response += u'%s tag\n\n' % tag
    else:
        response += u'Top Questions\n\n'
    
    for question in questions:
        if tag and tag not in question['tags']:
            continue
        response += question['summary'] + '\n'
        response += question['link'] + '\n'
        response += u'Tags: %s.   ' % ', '.join(question['tags'])
        response += u'(votes: %(votes)s, answers: %(answers)s, views: %(views)s)' % question
        response += '\n\n'
    
    return response.rstrip('\n\n')


class QuestionsParser(object):
    
    def parse(self, page, limit=100):
        questions = []
        for element in self.get_elements(page, limit):
            questions.append({
                'summary': self.get_summary(element),
                'link': self.get_link(element),
                'tags': self.get_tags(element),
                'votes': self.get_votes(element),
                'answers': self.get_answers(element),
                'views': self.get_views(element)
            })
        return questions
    
    def get_elements(self, page, limit):
        html = lhtml.fromstring(page)
        return html.cssselect('div.question-summary')[:limit]
    
    def get_summary(self, element):
        return element.cssselect('div.summary h3 a')[0].text_content()
    
    def get_link(self, element):
        return u'http://stackoverflow.com%s' % element.cssselect('div.summary h3 a')[0].attrib['href']
    
    def get_tags(self, element):
        tags = element.cssselect('div.tags')[0].attrib['class'].split()
        tags.remove('tags')
        return [ unicode(tag.lstrip('t-')) for tag in tags ]
    
    def get_views(self, element):
        return element.cssselect('div.views')[0].text_content().split()[0]
    
    def get_votes(self, element):
        return element.cssselect('div.votes div.mini-counts')[0].text_content()
    
    def get_answers(self, element):
        return element.cssselect('div.status div.mini-counts')[0].text_content()    
    


class TaggedQuestionsParser(QuestionsParser):
    
    def get_votes(self, element):
        return element.cssselect('span.vote-count-post strong')[0].text_content()
    
    def get_answers(self, element):
        return element.cssselect('div.status strong')[0].text_content()
    

