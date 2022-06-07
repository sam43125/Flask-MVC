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

def test_home_2(client):

    resp = client.post('/',data={'nm':'TSMC','from':'02.12.2022','to':'06.06.2022'})
    assert resp.status_code == 302
