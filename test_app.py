import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'JWKS Server is running' in rv.data

def test_auth_valid(client):
    rv = client.post('/auth')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'token' in data

def test_auth_expired(client):
    rv = client.post('/auth?expired=true')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'token' in data

def test_jwks(client):
    rv = client.get('/.well-known/jwks.json')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'keys' in data
    assert isinstance(data['keys'], list)