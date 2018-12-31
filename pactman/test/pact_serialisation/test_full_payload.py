from unittest.mock import Mock

from pactman import Consumer, Provider
from pactman.mock.pact_request_handler import construct_pact


def test_full_payload_v2():
    pact = Consumer('consumer').has_pact_with(Provider('provider'), version='2.0.0')
    (pact
        .given('UserA exists and is not an administrator')
        .upon_receiving('a request for UserA')
        .with_request('get', '/users/UserA')
        .will_respond_with(200, body={'username': 'UserA'}))
    result = construct_pact(Mock(consumer_name='consumer', provider_name='provider',
                                 version='2.0.0'), pact._interactions[0])
    assert result == {
        'consumer': {'name': 'consumer'},
        'provider': {'name': 'provider'},
        'interactions': [
            {
                'description': 'a request for UserA',
                'providerState': 'UserA exists and is not an administrator',
                'request': dict(method='get', path='/users/UserA'),
                'response': dict(status=200, body={'username': 'UserA'})
            }
        ],
        'metadata': dict(pactSpecification=dict(version='2.0.0'))
    }


def test_full_payload_v3():
    pact = Consumer('consumer').has_pact_with(Provider('provider'), version='3.0.0')
    (pact
     .given([{"name": "User exists and is not an administrator", "params": {"username": "UserA"}}])
     .upon_receiving('a request for UserA')
     .with_request('get', '/users/UserA')
     .will_respond_with(200, body={'username': 'UserA'}))
    result = construct_pact(Mock(consumer_name='consumer', provider_name='provider',
                                 version='3.0.0'), pact._interactions[0])
    assert result == {
        'consumer': {'name': 'consumer'},
        'provider': {'name': 'provider'},
        'interactions': [
            {
                'description': 'a request for UserA',
                'providerStates': [{
                    "name": "User exists and is not an administrator",
                    "params": {"username": "UserA"}
                }],
                'request': dict(method='get', path='/users/UserA'),
                'response': dict(status=200, body={'username': 'UserA'})
            }
        ],
        'metadata': dict(pactSpecification=dict(version='3.0.0'))
    }