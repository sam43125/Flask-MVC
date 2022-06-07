import pytest
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from app.model.Popularity import Popularity
def test_popularity():
    p = Popularity(Popularity.date,Popularity.TSMC,Popularity.AppliedMaterials,Popularity.ASML,Popularity.SUMCO)
    assert p != None

