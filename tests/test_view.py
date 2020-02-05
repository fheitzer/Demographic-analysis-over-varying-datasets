import sys
sys.path.append("..")
from view import View
from model import merge_all_data

"""
This is a collection of pytests for the model.py functionalities.
"""


def test_visualise():
    """Funtion to test the plots produced by view."""
    p = View(merge_all_data())
    p.visualise()
    assert str(type(p.lines[0])) == "<class 'bokeh.models.layouts.Panel'>", "Returned object is not a bokeh plot."

