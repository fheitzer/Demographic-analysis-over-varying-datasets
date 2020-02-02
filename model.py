import pandas as pd

if __name__ == "__main__":
    dataeurostat = pd.read_csv("data/demo_gind/demo_gind_1_Data.csv")
    print(dataeurostat)

    dataistat = pd.read_csv("data/ISTAT.csv")
    dataistat = pd.DataFrame(dataistat)
    dataistat = dataistat[dataistat["Territory"] == "Italy"]
    dataistat = dataistat[dataistat['Gender'] == "total"]
    dataistat = dataistat[dataistat['Select time'].str.contains('^\d*$', regex=True, na=False)]
    print(dataistat['Demographic data type'].drop_duplicates())

    #dataistat = dataistat.set_index(['Select time'])
    dataistat = dataistat.pivot_table('Value', ['Select time'], 'Demographic data type')
    dataistat = dataistat.sort_index()
    dataistat['population'] = dataistat[['population at the beginning of the period', 'population at end of the period']].mean(axis=1)
    dataistat = dataistat.drop(['population at the beginning of the period', 'population at end of the period'], axis=1)
    print(dataistat.head(20))
    print(dataistat.info())

    #dataistat = dataistat["Value"]
    #dataistat = pd.DataFrame(dataistat)
    #dataistat.columns = ["Population"]


