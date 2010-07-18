from eizzek.lib.plugins.stackoverflow import stackoverflow, build_response

def test_stackoverflow():
    response = stackoverflow('python')
    
    assert 'Stack Overflow: python tag' in response
    
    response = stackoverflow()
    
    assert 'Stack Overflow: Top Questions' in response