import pandas as pd
import plotly.graph_objects as go
import numpy as np

# read csv-file, set firs column as indices
coffee = pd.read_csv("../data/arabica_data_cleaned.csv", index_col=0)

# only keep columns "Country.of.Origin", "Producer", "Processing.Method", rename them
coffee_clean = coffee[["Country.of.Origin", "Producer", "Processing.Method"]]
coffee_clean.columns = ["Country of Origin", "Producer", "Processing Method"]

# plot histograms of the columns
for column in coffee_clean.columns:
    country_names = coffee_clean[column].dropna().unique()
    print(country_names)

    value_counts = coffee_clean[column].value_counts()
    print(value_counts)  # is a pandas series

    yvalues = []
    for country in country_names:
        yvalues.append(value_counts.loc[country])
    print(yvalues)

    data = [
            go.Bar(
                x=country_names,
                y=yvalues,
                marker_color="rgba(168, 0, 0, 1)",
            )
        ]

    layout = {
        "title": {
            "text": f"Histogram of {column}",
            "font_size": 30,
        },
        "plot_bgcolor": "rgba(0, 0, 0, 0.1)",  # Hintergrundfarbe
        "xaxis":{
            "color": "rgba(0, 0, 0, 1)",
            "title": {
                "text": column,
                "font_size": 20,
                "font_family": "Courier"
            },
            "showline": True,
            "linewidth": 1,
            "linecolor": "black",
            "mirror": False
        },
        "yaxis": {
            "showgrid": True,
            "gridwidth": 1,
            "gridcolor": "rgba(0, 0, 0, 0.2)",
            "color": "rgba(0,0,0,1)",
            "ticks": "outside",
            #"tickvals": [1, 5, 10],
            "title": {
                "text": "count",
                "font_size": 20,
                "font_family": "Courier",
            },
            "showline": True,
            "linewidth": 1,
            "linecolor": "black",
            "mirror": True,  # sagt ob rechts auch ein Strich ist
            # "type": "log"
        }
    }
    fig = go.Figure(data=data, layout=layout)
#     fig.show()

producer_counts = coffee_clean["Producer"].value_counts()
origin_counts = coffee_clean["Country of Origin"].value_counts()
list_of_countries = coffee_clean["Country of Origin"].dropna().unique()
method_counts = coffee_clean["Processing Method"].value_counts()

# remove outliers

# idea of Lotte
median = float(origin_counts.median())
yvalues_amend = []
for country in list_of_countries:       # country in list of countries
    if origin_counts.loc[country] > origin_counts.quantile(.9):   # larger than 9th quantile
        yvalues_amend.append(median)
    elif origin_counts.loc[country] < origin_counts.quantile(.1):     # smaller than 1st quantile
        yvalues_amend.append(median)
    else:
        yvalues_amend.append(origin_counts.loc[country])
print(yvalues_amend)

# countries of origin < 10

# producers with value 1
x = producer_counts[producer_counts == 1].index
for name in x:
    print(name)
    coffee_clean = coffee_clean[coffee_clean.Producer != name]
print(coffee_clean)
print(coffee_clean["Producer"].value_counts())  # geht nur no bis 2 -> alle mit Producer = 1 ist weg!

# processing method < 100



# identify
# Which countries have more than 10 and less than 30 entries?
smaller30 = origin_counts[30 > origin_counts]
andmorethan10 = smaller30[smaller30 > 10]
print(andmorethan10.index)  # out: list ['Uganda', 'Nicaragua', 'Kenya', 'El Salvador', 'Indonesia', 'China', 'Malawi']
# oder:
mask10 = origin_counts > 10
mask30 = origin_counts < 30
mask = mask10 & mask30
print(origin_counts[mask])

# Which is the producer with most entries?
print(producer_counts.idxmax())  # out: La Plata
# oder:
producer_counts.sort_values(inplace=True)
print(origin_counts.index[-1])

# What is the most common and least common "Processing Method"
print("most common:", method_counts.idxmax())
print("least common:", method_counts.idxmin())
