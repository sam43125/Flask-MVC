import pytest
from app import app
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_home_bad_http_method(client):
    resp = client.post('/')
    assert resp.status_code == 405


