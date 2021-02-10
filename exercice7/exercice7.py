import pandas as pd
import numpy as np
import ssl
import json
import urllib.request

# get COVID data from ECDC
covid_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
ssl._create_default_https_context = ssl._create_unverified_context
covid_json_unformated = urllib.request.urlopen(covid_url).read().decode("utf-8")
covid_json = json.loads(covid_json_unformated)
cdf = pd.DataFrame(covid_json['records'])

# rename columns
cdf.rename(
    columns={
        "dateRep": "date",
        "countriesAndTerritories": "countries",
        "geoId": "geo_id",
        "countryterritoryCode": "country_code",
        "popData2019": "pop_data_2019",
        "continentExp": "continent",
        "notification_rate_per_100000_population_14-days": "14d-incidence"
    },
    inplace=True
)

# oder mit neuer colnames-list übergeben: cdf.columns = ["date", "year_week", "cases_weekly", "deaths_weekly",
# "countries", "geo_id", "country_code", "pop_data_2019", "continent", "14d-incidence"]


# which columns have not been casted to an appropriate type during loading
print(cdf.info())  # date als object, 14d-incidence as object

# change wrong types
cdf["14d-incidence"] = pd.to_numeric(cdf["14d-incidence"])
cdf["date"] = pd.to_datetime(cdf["date"])
# print(cdf['date'].dt.day.head())  # sagt die Tage der ersten fünf Zeilen

# add column deltaTime_since_start_of_recording
start = cdf.loc[cdf["date"].idxmin(), "date"]  # findet kleinste Zeit und setzt sie als Start
cdf['t_since_start'] = cdf['date'] - start  # erstellt neue Spalte mit Zeit seit Beginn

# histograms for different columns or describe the df. Can you spot the inconsistency in the data? Fix it! :)
description = cdf.describe()  # negative values as min in death, cases, 14d-incidence, dates in future

# drop na values
cdf_clean = cdf.dropna()

# drop negative values
for column in ['deaths_weekly', 'cases_weekly', '14d-incidence']:
    mask = cdf_clean[column] >= 0
    cdf_clean = cdf_clean[mask]

# drop dates in future
mask_date = cdf_clean["date"] < cdf.loc[0, "date"].now()
cdf_clean = cdf_clean[mask_date]


# Identify those countries (grouped by continent) which showed the most drastic increase most drastic and decrease of
# the 14d-incidence within the different years since recording. Visualize intuitively!

cdf_clean_sort = cdf_clean.sort_values("date")

# group by continents and countries
grouped = cdf_clean_sort.groupby(["continent", "countries"])
grouped["14d-incidence"].idxmax()  # gibt: continent->country->idx aus cdf_clean für maximale 14d-incidence aus dem Land
# calculate difference


# groupby["continent", "countries"]
# Daten nach Datum sortieren, dann Differenz zu vorherigem Eintrag pd[col].diff["14d-incidence"] dann noch nan=0