import pytest
from pytrends.request import TrendReq
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

def test_pytrends():
    pytrends = TrendReq(hl='zh-TW', tz=-480)
    pytrends.build_payload(kw_list=['TSMC'], cat=0, timeframe='all', geo='', gprop='')
    results = pytrends.interest_over_time()
    assert len(results) > 0