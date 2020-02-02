import pandas as pd


def import_clean_istat():
    """Importing and cleaning ISTAT.
        returns istat as pandas.dataframe"""
    # Import
    istat = pd.read_csv("data/ISTAT.csv")

    # Drop column information that is not in our interest
    istat = istat[istat["Territory"] == "Italy"]
    istat = istat[istat['Gender'] == "total"]
    istat = istat[istat['Select time'].str.contains('^\d*$', regex=True, na=False)]

    # Reshape the table
    istat = istat.pivot_table('Value', ['Select time'], 'Demographic data type')
    istat = istat.sort_index()
    istat['population'] = istat[['population at the beginning of the period',
                                 'population at end of the period']].mean(axis=1)
    istat = istat.drop(['population at the beginning of the period', 'population at end of the period'], axis=1)

    return istat


if __name__ == "__main__":

    data_eurostat = import_clean_eurostat()
    data_istat = import_clean_istat()
    print(data_eurostat)
    print(data_istat)
