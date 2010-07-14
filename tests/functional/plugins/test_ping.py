from eizzek.lib.plugins.ping import ping


def test_ping():
    response = ping('igorsobreira.com')
    
    assert 'PING igorsobreira.com (67.18.187.198): 56 data bytes' in response