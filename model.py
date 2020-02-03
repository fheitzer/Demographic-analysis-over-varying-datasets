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
    istat.rename(columns={'Select time': 'Year', 'Territory': 'Country'}, inplace=True)
    istat = istat.pivot_table('Value', ['Country', 'Year'], 'Demographic data type')
    istat = istat.sort_index()

    # Merge Population columns
    istat['Population'] = istat[['population at the beginning of the period',
                                 'population at end of the period']].mean(axis=1)
    istat = istat.drop(['population at the beginning of the period', 'population at end of the period'], axis=1)

    # Renaming
    istat.rename(columns={'deaths': 'Deaths', 'emigrated to other countries': 'Emigration',
                          'immigrated from other countries': 'Immigration', 'live births': 'Births'}, inplace=True)

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
    eurostat_im.rename(columns={'Value': 'Immigration', 'GEO': 'Country', 'TIME': 'Year'}, inplace=True)
    eurostat_im.set_index(['Country', 'Year'], inplace=True)
    eurostat_im.sort_index(inplace=True)
    eurostat_im = pd.DataFrame(eurostat_im['Immigration'])

    eurostat_em = import_clean_eurostat('eurostat_emigration')
    eurostat_em.rename(columns={'Value': 'Emigration', 'GEO': 'Country', 'TIME': 'Year'}, inplace=True)
    eurostat_em.set_index(['Country', 'Year'], inplace=True)
    eurostat_em.sort_index(inplace=True)
    eurostat_em = pd.DataFrame(eurostat_em['Emigration'])

    return pd.concat([eurostat_pop, eurostat_im, eurostat_em], axis=1)


def import_clean_OECD(data_name):
    """Importing and cleaning OECD.
        returns istat as pandas.dataframe"""

    oecd = pd.read_csv(f'data/OECD_{data_name}.csv')
    oecd.rename(columns={'LOCATION': 'Country', 'TIME': 'Year', 'Value': data_name}, inplace=True)
    oecd[data_name] = oecd[data_name].apply(lambda value: float(value * 1000000))
    oecd = oecd[oecd['Country'].apply(lambda x: len(x) == 3)]
    oecd = oecd[oecd['Country'].apply(
        lambda x: pc.country_alpha2_to_continent_code(country_2_code=pc.country_alpha3_to_country_alpha2(x)) == 'EU')]


    oecd['Country'] = oecd['Country'].apply(lambda x: pc.map_country_alpha3_to_country_name()[x])
    oecd.set_index(['Country', 'Year'], inplace=True)
    oecd.sort_index(inplace=True)
    oecd = pd.DataFrame(oecd[data_name])

    return oecd


def merge_oecd() -> pd.DataFrame:
    oecd_birth = import_clean_OECD('Births')
    oecd_pop = import_clean_OECD('Population')

    oecd = pd.concat([oecd_pop, oecd_birth], axis=1)

    return oecd

if __name__ == "__main__":

    oecd = merge_oecd()
    print(oecd)
    eurostat = merge_eurostat()
    print(eurostat)
    istat = import_clean_istat()
    print(istat)
    print(pd.concat([oecd, istat, eurostat]))