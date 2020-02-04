import sys
sys.path.append("..")
from view import visualise
from model import merge_datasets

def test_visualise():
    """Funtion to test the plots produced by view."""
    p = visualise(merge_datasets())
    assert str(type(p)) == "<class 'bokeh.plotting.figure.Figure'>", "Returned object is not a bokeh plot."
