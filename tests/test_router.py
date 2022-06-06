import pytest
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from app.controller import router


def test_get_interest_over_time():
    info = router.get_interest_over_time()
    assert len(info) > 0
