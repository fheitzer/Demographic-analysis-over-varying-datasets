from model import merge_all_data
import pandas as pd
from view import View


if __name__ == "__main__":
    # Get the data
    data = merge_all_data()

    # Lets visualise it
    viewer = View(data)
    viewer.visualise()
