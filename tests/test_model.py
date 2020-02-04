import sys
sys.path.append("..")
import model
import numpy

"""
This is a collection of pytests for the model.py functionalities.
"""


def test_import_clean_istat():
    data = model.import_clean_istat()
    assert data.loc[('Italy', 2011)].Deaths == 139009
