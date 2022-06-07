import pytest
import os
import sys
from app import app
from app import db
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from app.controller import router
from app.controller.router import GoogleCrawler
from app.model.Popularity import Popularity

def test_get_interest_over_time():
    info = router.get_interest_over_time()
    assert len(info) > 0

def test_popularity_to_dataframe():
    df = router.popularity_to_dataframe(Popularity.query.all())
    assert len(df) > 0

def test_utility_processor():
    d = router.utility_processor()
    assert len(d) > 0

def test_requests_count():
    respone = router.requests_count()
    assert respone.status_code == 200


def test_get_source():
    crawler = GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    assert response.status_code == 200

def test_google_search():
    crawler = GoogleCrawler()
    query = "TSMC Ingas"
    results = crawler.google_search(query)
    assert len(results) > 0

def test_html_parser():
    crawler = GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    results = soup.findAll("div")
    assert len(results) > 0

def test_word_count():
    crawler = GoogleCrawler()
    text = "Taiwan’s TSMC confident its chips will outperform Intel's new TSMC product line"
    d = crawler.word_count(text)
    assert d['Taiwan'] == 1
    assert d['TSMC'] == 2
    assert d['confident'] == 1
    assert d['chips'] == 1
    assert d['outperform'] == 1
    assert d['Intel'] == 1
    assert d['new'] == 1
    assert d['product'] == 1
    assert d['line'] == 1

def test_html_getText():
    crawler = GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    assert len(orignal_text) > 0

#router.google_search("TSMC","02.12.2022","06.06.2022")
@pytest.fixture
def client():
    return app.test_client()
'''
def test_list(client):
    resp = client.get('/google_search/TSMC/02.12.2022/06.06.2022')
    assert resp.status_code == 200
    resp2 = client.get('/google_search/TSMC')
    assert resp2.status_code == 200
'''