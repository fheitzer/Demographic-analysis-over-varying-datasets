import pandas as pd
import pycountry_convert as pc
import regex as re


def import_clean_istat() -> pd.DataFrame:
    """Importing and cleaning ISTAT.
        returns istat as pandas.dataframe"""
    # Import
    istat = pd.read_csv("data/ISTAT.csv")

    # Drop column information that is not in our interest
    istat = istat[istat["Territory"] == "Italy"]
    istat = istat[istat['Gender'] == "total"]
    istat = istat[istat['Select time'].str.contains(r'^\d*$', regex=True, na=False)]

    # Reshape the table
    istat.rename(columns={'Select time': 'Year', 'Territory': 'Country'}, inplace=True)
    istat['Year'] = istat['Year'].apply(lambda x: int(x))
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


def import_clean_eurostat(data_name: str, mode: int) -> pd.DataFrame:
    """Importing and cleaning EUROSTAT.
        returns EUROSTAT as pandas.dataframe"""

    # Import
    eurostat = pd.read_csv(f"data/eurostat_{data_name}.csv")

    # Clean
    eurostat = eurostat[eurostat['Value'] != ':']
    eurostat['Value'] = eurostat['Value'].apply(lambda x: float(x.replace(",", "")))

    if mode == 0:
        eurostat['INDIC_DE'] = eurostat['INDIC_DE'].apply(lambda x: x[:-8])
        eurostat = eurostat.pivot_table('Value', ['GEO', 'TIME'], 'INDIC_DE', aggfunc='first')
        eurostat.rename(columns={'Average population': data_name, 'Live births': 'Births'}, inplace=True)
        eurostat.sort_index(inplace=True)

    elif mode == 1:
        eurostat.rename(columns={'Value': data_name, 'GEO': 'Country', 'TIME': 'Year'}, inplace=True)
        eurostat.set_index(['Country', 'Year'], inplace=True)
        eurostat.sort_index(inplace=True)
        eurostat = pd.DataFrame(eurostat[data_name])

    return eurostat


def merge_eurostat() -> pd.DataFrame:
    """Get eurostat datasets and concatenate them."""

    # Import
    eurostat_pop = import_clean_eurostat('Population', 0)
    eurostat_im = import_clean_eurostat('Immigration', 1)
    eurostat_em = import_clean_eurostat('Emigration', 1)

    return pd.concat([eurostat_pop, eurostat_im, eurostat_em], axis=1)


def import_clean_oecd(data_name) -> pd.DataFrame:
    """Importing and cleaning OECD.
        returns istat as pandas.dataframe"""

    # Import, Rename, adjust values in million
    oecd = pd.read_csv(f'data/OECD_{data_name}.csv')
    oecd.rename(columns={'LOCATION': 'Country', 'TIME': 'Year', 'Value': data_name}, inplace=True)
    oecd[data_name] = oecd[data_name].apply(lambda value: float(value * 1000000))

    # Kick out every country with the wrong code len (they're not in europe anyways) & not in europe
    oecd = oecd[oecd['Country'].apply(lambda x: len(x) == 3)]
    oecd = oecd[oecd['Country'].apply(
        lambda x: pc.country_alpha2_to_continent_code(country_2_code=pc.country_alpha3_to_country_alpha2(x)) == 'EU')]

    # Turn country codes to full country names
    oecd['Country'] = oecd['Country'].apply(lambda x: pc.map_country_alpha3_to_country_name()[x])
    oecd.set_index(['Country', 'Year'], inplace=True)
    oecd.sort_index(inplace=True)
    oecd = pd.DataFrame(oecd[data_name])

    return oecd


def merge_oecd() -> pd.DataFrame:
    """Import oecd datasets & concatenate"""

    # Import
    oecd_pop = import_clean_oecd('Population')
    oecd_birth = import_clean_oecd('Births')

    # Concatenate
    oecd = pd.concat([oecd_pop, oecd_birth], axis=1)
    oecd.sort_index(inplace=True)

    return oecd


def merge_datasets() -> pd.DataFrame:
    """Concatinates according to indexes and then takes
    the mean if we have multiple values for one year."""

    # Load datasets
    oecd = merge_oecd()
    eurostat = merge_eurostat()
    istat = import_clean_istat()

    # Concatinate datasets
    merge = pd.concat([oecd, istat, eurostat])
    merge.sort_index(inplace=True)

    # Save index, groupby index to average multiple values, get old index without duplicates
    index = merge.index.drop_duplicates()
    merge = merge.groupby(merge.index).mean()
    merge.sort_index(inplace=True)
    merge.set_index(index, inplace=True)
    merge.reset_index(inplace=True)

    # Kicking out general Europe entries
    merge = merge[~merge.Country.str.contains("urope")]
    return merge


if __name__ == "__main__":
    data = merge_datasets()
    print(data)