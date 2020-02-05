import model
import pandas as pd
from view import View

if __name__ == "__main__":
    oecd = model.OECDGatherer()
    oecd.gather('Population')
    oecd.gather('Births')
    oecd.merge()

    istat = model.ISTATGatherer()
    istat.gather()

    eurostat = model.EUROSTATGatherer()
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
    merge = data[~data.Country.str.contains("urope")]


    viewer = View(data)
    viewer.visualise()
