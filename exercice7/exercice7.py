import pandas as pd
import numpy as np
import ssl
import json
import urllib.request
import plotly.graph_objects as go

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
for i in range(0, cdf.shape[0]):
    cdf.loc[i, 'year'] = cdf.loc[i, 'date'].year  # fügt neue Spalte fürs Jahr dazu

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
cdf_clean = cdf_clean[mask_date]  # cdf_clean hat keine neuen Indices! Indices wie bei cdf!

# Identify those countries (grouped by continent) which showed the most drastic increase most drastic and decrease of
# the 14d-incidence within the different years since recording. Visualize intuitively!

cdf_clean_sort = cdf_clean.sort_values("date")  # cdf_clean_sort hat au keine neuen Indices! Indices wie bei cdf!

# erster Versuch
# # group by continents and countries
# grouped = cdf_clean_sort.groupby(["continent", "countries"])
# grouped["14d-incidence"].idxmax()  # gibt: continent->country->idx aus cdf für maximale 14d-incidence aus dem Land
# # calculate difference
#
# x = grouped.get_group(("Africa", "Algeria"))
# # Daten nach Datum sortieren, dann Differenz zu vorherigem Eintrag pd[col].diff() dann noch nan=0
# x["inc_diff"] = x["14d-incidence"].diff()
# x["inc_diff"].fillna(0, inplace=True)


def give_deltainc_percontinent(cdf_clean_sort):
    """

    Args:
        cdf_clean_sort: pandas dataframe

    Returns:
        final_pandas: df containing countries with highest/lowest increase per continent

    """
    a = np.empty((0, 4))
    for continent, cont_grp in cdf_clean_sort.groupby(["continent"]):
        # print(continent)
        for country, country_grp in cont_grp.groupby(["countries"]):
            # print(country)
            diffs = country_grp["14d-incidence"].diff().fillna(0)
            min_dif = min(diffs)
            max_dif = max(diffs)
            a = np.append(a, [[continent, country, min_dif, max_dif]], axis=0)

    a_pandas = pd.DataFrame(a)
    a_pandas.columns=["continent", "country", "min_difs", "max_difs"]
    a_pandas["min_difs"] = pd.to_numeric(a_pandas["min_difs"])
    a_pandas["max_difs"] = pd.to_numeric(a_pandas["max_difs"])
    country_lowest_diff = a_pandas.loc[a_pandas["min_difs"].idxmin(), "country"]
    min_dif_value = a_pandas["min_difs"].min()
    print(f"The country with the most drastic decrease of the 14d-incidence is: {country_lowest_diff} (value: {min_dif_value})")
    country_highest_diff = a_pandas.loc[a_pandas["max_difs"].idxmax(), "country"]
    max_dif_value = a_pandas["max_difs"].max()
    print(f"The country with the most drastic increase of the 14d-incidence is: {country_highest_diff} (Value: {max_dif_value})")

    final = np.empty((0, 5))
    for continent, grp_continent in a_pandas.groupby("continent"):
        index_min = grp_continent["min_difs"].idxmin()
        index_max = grp_continent["max_difs"].idxmax()
        final = np.append(final, [[continent,
                                  a_pandas.loc[index_min, "country"],
                                  a_pandas.loc[index_min, "min_difs"],
                                  a_pandas.loc[index_max, "country"],
                                  a_pandas.loc[index_max, "max_difs"]]], axis=0)

    final_pandas = pd.DataFrame(final)
    final_pandas.columns = ["continent", "min_country", "min_value", "max_country", "max_value"]
    return final_pandas

def give_deltainc_percontinent_andyear(cdf_clean_sort):
    """

    Args:
        cdf_clean_sort: pandas dataframe

    Returns:
        final_pandas: df containing countries with highest/lowest increase per continent and year

    """
    a = np.empty((0, 5))
    for continent, cont_grp in cdf_clean_sort.groupby(["continent"]):
        # print(continent)
        for country, country_grp in cont_grp.groupby(["countries"]):
            # print(country)
            for year, year_grp in country_grp.groupby(["year"]):
                diffs = year_grp["14d-incidence"].diff().fillna(0)
                min_dif = min(diffs)
                max_dif = max(diffs)
                a = np.append(a, [[continent, country, min_dif, max_dif, year]], axis=0)

    a_pandas = pd.DataFrame(a)
    a_pandas.columns=["continent", "country", "min_difs", "max_difs", "year"]
    a_pandas["min_difs"] = pd.to_numeric(a_pandas["min_difs"])
    a_pandas["max_difs"] = pd.to_numeric(a_pandas["max_difs"])

    final = np.empty((0, 6))
    for continent, grp_continent in a_pandas.groupby("continent"):
        for year, year_grp in grp_continent.groupby("year"):
            index_min = year_grp["min_difs"].idxmin()
            index_max = year_grp["max_difs"].idxmax()
            final = np.append(final, [[year, continent,
                                      a_pandas.loc[index_min, "country"],
                                      a_pandas.loc[index_min, "min_difs"],
                                      a_pandas.loc[index_max, "country"],
                                      a_pandas.loc[index_max, "max_difs"]]], axis=0)

    final_pandas = pd.DataFrame(final)
    final_pandas.columns = ["year", "continent", "min_country", "min_value", "max_country", "max_value"]
    final_pandas["min_value"] = pd.to_numeric(final_pandas["min_value"])
    final_pandas["max_value"] = pd.to_numeric(final_pandas["max_value"])
    final_pandas["year"] = pd.to_numeric(final_pandas["year"])
    country_lowest_diff = final_pandas.loc[final_pandas["min_value"].idxmin(), "min_country"]
    min_dif_value = final_pandas["min_value"].min()
    print(
        f"The country with the most drastic decrease of the 14d-incidence is: {country_lowest_diff} (value: {min_dif_value})")
    country_highest_diff = final_pandas.loc[final_pandas["max_value"].idxmax(), "max_country"]
    max_dif_value = final_pandas["max_value"].max()
    print(
        f"The country with the most drastic increase of the 14d-incidence is: {country_highest_diff} (Value: {max_dif_value})")

    return final_pandas

# plotting
# data = [
#     go.Bar(
#         x=country_names,
#         y=yvalues,
#         marker_color="rgba(168, 0, 0, 1)",
#     )
# ]
# fig = go.Figure(data=data)
# fig.show()

if __name__ == '__main__':
    print(give_deltainc_percontinent(cdf_clean_sort))
