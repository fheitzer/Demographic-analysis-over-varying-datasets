import sys
sys.path.append("..")
import model
import numpy

"""
This is a collection of pytests for the model.py functionalities.
"""


def test_import_clean_istat():
    assert model.import_clean_istat().loc[('Italy', 2011)]['Deaths'] == 139009.0,\
        "Value is not right"


def test_merge_datasets():
    assert type(model.merge_datasets().loc[('Italy', 2011)]['Population']) == numpy.float64
