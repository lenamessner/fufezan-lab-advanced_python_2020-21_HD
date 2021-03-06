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
        "cases": "cases_weekly",
        "deaths": "deaths_weekly",
        "geoId": "geo_id",
        "countryterritoryCode": "country_code",
        "popData2019": "pop_data_2019",
        "continentExp": "continent",
        "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000": "14d-incidence"
    },
    inplace=True
)

# oder mit neuer colnames-list übergeben: cdf.columns = ["date", "year_week", "cases_weekly", "deaths_weekly",
# "countries", "geo_id", "country_code", "pop_data_2019", "continent", "14d-incidence"]


# which columns have not been casted to an appropriate type during loading
print(cdf.info())  # date als object, 14d-incidence as object

# change wrong types
cdf["14d-incidence"] = pd.to_numeric(cdf["14d-incidence"])
cdf["date"] = pd.to_datetime(cdf["date"], format='%d/%m/%Y',
                             errors='raise')  # format muss angegeben werden, weil er sonst random
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
    a_pandas.columns = ["continent", "country", "min_difs", "max_difs"]
    a_pandas["min_difs"] = pd.to_numeric(a_pandas["min_difs"])
    a_pandas["max_difs"] = pd.to_numeric(a_pandas["max_difs"])

    # to print country with highest/lowest increase worldwide, not sorted by year: country_lowest_diff =
    # a_pandas.loc[a_pandas["min_difs"].idxmin(), "country"] min_dif_value = a_pandas["min_difs"].min() print( f"The
    # country with the most drastic decrease of the 14d-incidence is: {country_lowest_diff} (value: {
    # min_dif_value})") country_highest_diff = a_pandas.loc[a_pandas["max_difs"].idxmax(), "country"] max_dif_value =
    # a_pandas["max_difs"].max() print( f"The country with the most drastic increase of the 14d-incidence is: {
    # country_highest_diff} (Value: {max_dif_value})")

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
    a_pandas.columns = ["continent", "country", "min_difs", "max_difs", "year"]
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

    return final_pandas


def give_deltainc_peryear(cdf_clean_sort):
    """
    function prints most drastic increase/decrease of 14d-incidence per year
    Args:
        cdf_clean_sort: pandas dataframe

    Returns:

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
    a_pandas.columns = ["continent", "country", "min_difs", "max_difs", "year"]
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

    for year, year_grp2 in final_pandas.groupby("year"):
        country_lowest_diff = year_grp2.loc[year_grp2["min_value"].idxmin(), "min_country"]
        min_dif_value = year_grp2.loc[year_grp2["min_value"].idxmin(), "min_value"]
        year = int(year)
        print(
            f"In {year}, the country with the most drastic decrease of the 14d-incidence is: {country_lowest_diff} (value: {min_dif_value})")
        country_highest_diff = year_grp2.loc[year_grp2["max_value"].idxmax(), "max_country"]
        max_dif_value = year_grp2["max_value"].max()
        print(
            f"In {year}, the country with the most drastic increase of the 14d-incidence is: {country_highest_diff} (Value: {max_dif_value})")


def get_values_for_plotting(cdf_clean_sort):
    Europe = cdf_clean_sort.groupby("continent").get_group("Europe")
    xvalues = pd.DataFrame()
    yvalues = pd.DataFrame()
    for country, grp_country in Europe.groupby("countries"):
        for i in range(grp_country.shape[0]):
            date = grp_country.iloc[i, 0]
            incidence = grp_country.iloc[i, 11]  # new df requires column 11 instead of 9
            xvalues.loc[i, country] = date
            yvalues.loc[i, country] = incidence
    return xvalues, yvalues


def plot_values(xvalues, yvalues):
    """
    plots given x and y values as lineplot
    Args:
        xvalues: list of dates
        yvalues: list of corresponding 14d-incidence

    Returns:

    """
    layout = {
        "title": {
            "text": f"14d-incidence in European Countries",
            "font_size": 30,
        },
        "xaxis": {
            "title": {
                "text": "date",
                "font_size": 20,
                "font_family": "Courier"
            }
        },
        "yaxis": {
            "title": {
                "text": "14d-incidence",
                "font_size": 20,
                "font_family": "Courier",
            }
        }
    }
    fig = go.Figure(layout=layout)
    for country in xvalues.columns:
        fig.add_trace(go.Scatter(x=xvalues[country],
                                 y=yvalues[country],
                                 name=country))
    fig.show()


# Create a radial plot of death rate / 100000 people (see popData2019), where one year completes a circle,
# i.e. 360˚. Visualize the recorded years for Italy, Germany, Sweden and Greece. Hint you might need to turn the
# dateTime into day within the year (%j) and adjust 365 to 360 degrees.

# deaths/100.000 people = (deaths/pop)*100.000
cdf_clean_sort["death_perpeople"] = (cdf_clean_sort["deaths_weekly"] / cdf_clean_sort["pop_data_2019"]) * 100000
cdf_clean_sort["t_since_start"] = pd.to_numeric(cdf_clean_sort["t_since_start"].dt.days)
cdf_clean_sort["t_percent"] = cdf_clean_sort["t_since_start"] / 365
country_groups = cdf_clean_sort.groupby("countries")


def plot_radial(list_of_countries):
    """
    creates a radial plot showing the death rate per 100,000 people in selected countries as radial plot
    Args:
        list_of_countries: list of countries that should be plotted (countries as string)

    Returns:

    """
    fig = go.Figure()

    for country in list_of_countries:
        r_values = []
        theta_values = []
        current_country = country_groups.get_group(country)
        # only keep rows for measurements within first year since start of measurement:
        current_country_firstyear = current_country[current_country["t_since_start"] < 366]
        for row in range(current_country_firstyear.shape[0]):
            r_values.append(current_country_firstyear.iloc[row, 13])  # death_perpeople
            theta_values.append(current_country_firstyear.iloc[row, 14] * 360)  # percent*grad

        fig.add_trace(go.Scatterpolargl(r=r_values,
                                        theta=theta_values,
                                        name=country,
                                        mode='markers'))

    fig.update_layout(title={"text": "death rate per 100,000 people in the first year of measurements",
                      "font": {"size": 20}}
                      )
    fig.update_layout(title_xref='paper')  # titel ned so weit links
    fig.update_layout(legend_x=0.8)  # legende weiter links
    fig.update_polars(radialaxis_title_text="death rate")
    fig.update_polars(angularaxis_tickmode='array')
    fig.update_polars(angularaxis_tickvals=[0, 41.425, 82.849, 124.274, 165.699, 207.123, 248.550, 289.973, 331.397])  # an den Stellen gibts ticks
    fig.update_polars(angularaxis_ticktext=["0 weeks since start of measurements", 6, 12, 18, 24, 30, 36, 42, 48])  # Beschriftung für die ticks

    fig.show()


if __name__ == '__main__':
    give_deltainc_percontinent(cdf_clean_sort)
    give_deltainc_percontinent_andyear(cdf_clean_sort)
    give_deltainc_peryear(cdf_clean_sort)
    final_pandas = give_deltainc_percontinent_andyear(cdf_clean_sort)
    print(final_pandas)
    xvalues = get_values_for_plotting(cdf_clean_sort)[0]
    yvalues = get_values_for_plotting(cdf_clean_sort)[1]
    plot_values(xvalues, yvalues)
    plot_radial(["Greece", "Italy", "Sweden", "Germany"])
    print("hi")
