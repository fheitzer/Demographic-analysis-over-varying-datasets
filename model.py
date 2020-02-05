import pandas as pd
import pycountry_convert as pc
import regex as re


class DataGatherer:

    def __init__(self):
        self.data = list()

    def gather(self, data_name):
        """Gather data from in a similiar format
            from the same source in a pandas dataframe."""
        pass

    def merge(self):
        """Merge the gathered datasets."""
        pass


class ISTATGatherer(DataGatherer):

    def __init__(self):
        super().__init__()

    def gather(self, data_name=None):
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

        self.data = istat


class EUROSTATGatherer(DataGatherer):

    def __init__(self):
        super().__init__()

    def gather(self, data_name):
        """Importing and cleaning EUROSTAT.
            returns EUROSTAT as pandas.dataframe"""

        # Import
        eurostat = pd.read_csv(f"data/eurostat_{data_name}.csv")

        # Clean
        eurostat = eurostat[eurostat['Value'] != ':']
        eurostat['Value'] = eurostat['Value'].apply(lambda x: float(x.replace(",", "")))

        if data_name[0] == 'P':
            eurostat['INDIC_DE'] = eurostat['INDIC_DE'].apply(lambda x: x[:-8])
            eurostat = eurostat.pivot_table('Value', ['GEO', 'TIME'], 'INDIC_DE', aggfunc='first')
            eurostat.rename(columns={'Average population': data_name, 'Live births': 'Births'}, inplace=True)
            eurostat.sort_index(inplace=True)

        else:
            eurostat.rename(columns={'Value': data_name, 'GEO': 'Country', 'TIME': 'Year'}, inplace=True)
            eurostat['Country'] = eurostat['Country'].apply(lambda x: str(x).split(' ')[0] if re.match(r'[France|Germany].*', str(x)) else x)
            eurostat.set_index(['Country', 'Year'], inplace=True)
            eurostat.sort_index(inplace=True)
            eurostat = pd.DataFrame(eurostat[data_name])

        self.data.append(eurostat)

    def merge(self):
        self.data = pd.concat(self.data, axis=1)
        self.data.sort_index(inplace=True)

    #def _del_desc(self, x):
     #   if re.match(r'.*\(.*\)', x):
      #      dummy = x.split()
       #     return
        #    else x


class OECDGatherer(DataGatherer):

    def __init__(self):
        super().__init__()

    def gather(self, data_name):
        """Importing and cleaning OECD.
                returns istat as pandas.dataframe"""

        # Import, Rename, adjust values in million
        oecd = pd.read_csv(f'data/OECD_{data_name}.csv')
        oecd.rename(columns={'LOCATION': 'Country', 'TIME': 'Year', 'Value': data_name}, inplace=True)
        oecd['Country'] = oecd['Country'].apply(
            lambda x: x.split(' ')[0] if re.match(r'[France|Germany].*', x) else x)

        oecd[data_name] = oecd[data_name].apply(lambda value: float(value * 1000000))

        # Kick out every country with the wrong code len (they're not in europe anyways) & not in europe
        oecd = oecd[oecd['Country'].apply(lambda x: len(x) == 3)]
        oecd = oecd[oecd['Country'].apply(
            lambda x: pc.country_alpha2_to_continent_code(
                country_2_code=pc.country_alpha3_to_country_alpha2(x)) == 'EU')]

        # Turn country codes to full country names
        oecd['Country'] = oecd['Country'].apply(lambda x: pc.map_country_alpha3_to_country_name()[x])
        oecd.set_index(['Country', 'Year'], inplace=True)
        oecd.sort_index(inplace=True)
        oecd = pd.DataFrame(oecd[data_name])

        self.data.append(oecd)

    def merge(self):
        self.data = pd.concat(self.data, axis=1)
        self.data.sort_index(inplace=True)


def merge_all_data():
    """Use all the different gatherers to get a whole dataframe."""

    oecd = OECDGatherer()
    oecd.gather('Population')
    oecd.gather('Births')
    oecd.merge()

    istat = ISTATGatherer()
    istat.gather()

    eurostat = EUROSTATGatherer()
    eurostat.gather('Population')
    eurostat.gather('Immigration')
    eurostat.gather('Emigration')
    eurostat.merge()

    # Concatinate datasets
    data = pd.concat([oecd.data, istat.data, eurostat.data])
    data.sort_index(inplace=True)

    # Save index, groupby index to average multiple values, get old index without duplicates
    index = data.index.drop_duplicates()
    data = data.groupby(data.index).mean()
    data.sort_index(inplace=True)
    data.set_index(index, inplace=True)
    data.reset_index(inplace=True)

    # Kicking out general Europe entries
    data = data[~data.Country.str.contains("urope")]

    return data
