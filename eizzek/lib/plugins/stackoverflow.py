from lxml import html as lhtml

from eizzek.lib.decorators import plugin


# @plugin(r'^stackoverflow(?P<tag>.+)?$')
# def stackoverflow(tag=None):


def parse(page):
    
    html = lhtml.fromstring(page)
    elements = html.cssselect('div.question-summary')
    
    questions = []
    for element in elements:
        tags = element.cssselect('div.tags')[0].attrib['class'].split()
        tags.remove('tags')
        tags = [ unicode(tag.lstrip('t-')) for tag in tags ]
        
        summary = element.cssselect('div.summary h3 a')[0]
        
        questions.append({
            'summary': summary.text_content(),
            'link': u'http://stackoverflow.com%s' % summary.attrib['href'],
            'tags': tags,
            'votes': element.cssselect('span.vote-count-post strong')[0].text_content(),
            'answers': element.cssselect('div.status strong')[0].text_content(),
            'views': element.cssselect('div.views')[0].text_content().split()[0]
        })
    
    return questions
    