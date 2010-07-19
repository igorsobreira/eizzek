from eizzek.lib.plugins.stackoverflow import stackoverflow, build_response

def test_index():
    response = stackoverflow()
    questions = response.split('\n\n')
        
    assert 'Stack Overflow: Top Questions' in response
    assert 51 == len(questions)     # 50 + header


def test_index_limited():
    response = stackoverflow(limit=10)
    questions = response.split('\n\n')
    
    assert 'Stack Overflow: Top Questions' in response
    assert 11 == len(questions)


def test_tagged():
    response = stackoverflow(tag='python')
    questions = response.split('\n\n')
        
    assert 'Stack Overflow: python tag' in response

def test_tagged_limited():
    response = stackoverflow(tag='python', limit=3)
    questions = response.split('\n\n')
        
    assert 'Stack Overflow: python tag' in response
    assert 4 == len(questions)    
