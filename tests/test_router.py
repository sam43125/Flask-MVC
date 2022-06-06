import pytest
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from app.controller import router
from app.model.Popularity import Popularity
#from app import app, db
def test_get_interest_over_time():
    info = router.get_interest_over_time()
    assert len(info) > 0

def test_popularity_to_dataframe():
    df = router.popularity_to_dataframe(Popularity.query.all())
    assert len(df) > 0

def test_utility_processor():
    d = router.utility_processor()
    assert len(d) > 0