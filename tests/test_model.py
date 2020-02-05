import sys
sys.path.append("..")
from model import merge_all_data
import numpy

"""
This is a collection of pytests for the model.py functionalities.
"""


def test_merge_all_data():
    data = merge_all_data()
    print(data.Country.drop_duplicates())
    data = data[(data['Country'] == 'Italy') & (data['Year'] == 2011)]
    print(data)
    assert float(data.Deaths) == 366218.0

