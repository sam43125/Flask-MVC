import pytest
from app import app
from app.model.Popularity import Popularity
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

@pytest.fixture
def client():
    return app.test_client()

def test_list(client):
    Popularity.query.delete()
    resp = client.get('/list')
    assert resp.status_code == 200

def test_list_bad_http_method(client):
    resp = client.post('/list')
    assert resp.status_code == 405