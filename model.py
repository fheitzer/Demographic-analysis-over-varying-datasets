import pandas as pd
import pycountry_convert as pc


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
    istat['Population'] = istat[['population at the beginning of the period',
                                 'population at end of the period']].mean(axis=1)
    istat = istat.drop(['population at the beginning of the period', 'population at end of the period'], axis=1)

    return istat


def import_clean_eurostat(data_name: str):
    """Importing and cleaning EUROSTAT.
        returns EUROSTAT as pandas.dataframe"""

    # Import
    eurostat = pd.read_csv(f"data/{data_name}.csv")

    # Clean
    eurostat = eurostat[eurostat['Value'] != ':']
    eurostat['Value'] = eurostat['Value'].apply(lambda x: float(x.replace(",", "")))

    return eurostat


def merge_eurostat():

    eurostat_pop = import_clean_eurostat('eurostat_population')
    eurostat_pop['INDIC_DE'] = eurostat_pop['INDIC_DE'].apply(lambda x: x[:-8])
    eurostat_pop = eurostat_pop.pivot_table('Value', ['GEO', 'TIME'], 'INDIC_DE', aggfunc='first')
    eurostat_pop.rename(columns={'Average population': 'Population'}, inplace=True)

    eurostat_im = import_clean_eurostat('eurostat_immigration')
    eurostat_im = eurostat_im.pivot_table('Value', ['TIME'], 'GEO', aggfunc='first')

    eurostat_em = import_clean_eurostat('eurostat_emigration')
    eurostat_em = eurostat_em.pivot_table('Value', ['TIME'], 'GEO', aggfunc='first')



    print(eurostat_im)
    print(eurostat_em)
    print(eurostat_pop)




if __name__ == "__main__":

    merge_eurostat()