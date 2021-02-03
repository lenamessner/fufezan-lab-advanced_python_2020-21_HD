import pandas as pd
import plotly.graph_objects as go


# return hydropathy values according to sequence
def give_hydropathy_value(pure_sequence="", mapping_dict=None):
    if mapping_dict is None:
        mapping_dict={}
    hydropathy_values = []
    for aa in pure_sequence[:]:
        hydropathy_values.append(mapping_dict[str(aa)])
    return hydropathy_values


# plot hydropathy list
def plot_hydropathy(hydropathy_list=None, xvalues=None, title="", xtitle=""):
    if hydropathy_list is None:
        hydropathy_list = []
    if xvalues is None:
        xvalues = []
    data = [
        go.Bar(
            x=xvalues,
            y=hydropathy_list,
            marker_color="rgba(168, 0, 0, 1)",
        )
    ]

    layout = {
        "title": {
            "text": title,
            "font_size": 30,
        },
        "plot_bgcolor": "rgba(0, 0, 0, 0.1)",  # Hintergrundfarbe
        "xaxis":{
            "color": "rgba(0, 0, 0, 1)",
            "title": {
                "text": xtitle,
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
                "text": "hydopathy",
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
    fig.show()


# hydropathy list based on sliding window (average h value in window, length as arg)
def give_sliding_hydropathy_value(pure_sequence="", mapping_dict=None, window_size=0):
    if mapping_dict is None:
        mapping_dict={}
    average_hydropathy_values = []
    for pos, aa in enumerate(pure_sequence):
        if pos > len(pure_sequence)-window_size:
            break
        values = 0
        for subseq_aa in pure_sequence[pos:pos+window_size]:
            values += mapping_dict[str(subseq_aa)]
        average_value = values/window_size
        average_hydropathy_values.append(average_value)
    return (average_hydropathy_values)


if __name__ == '__main__':
    aap = "../data/amino_acid_properties.csv"

    genseq = "GP183_human.fasta"

    # create mapping_dict from csv-file with aap
    aap_df = pd.read_csv(aap)
    mapping_dict = {}
    for aa in range(len(aap_df.index)):
        for hydroind in range(len(aap_df.index)):
            mapping_dict[str(aap_df.loc[aa, '1-letter code'])] = aap_df.loc[
                aa, 'hydropathy index (Kyte-Doolittle method)']
    # print(mapping_dict)

    # extract sequence from fasta as string
    with open(genseq) as genseq_fasta:
        pure_sequence = ""
        for row in genseq_fasta:
            if not row[0] == ">":
                pure_sequence += row.replace("\n", "")
    # print(pure_sequence)

    xvalues=[]
    for pos in range(len(pure_sequence)):
        xvalues.append(pos)
    print(xvalues)

    hydropathy_values = give_hydropathy_value(pure_sequence, mapping_dict)
    print(hydropathy_values)
    plot_hydropathy(hydropathy_values, xvalues, "Hydropathy Index of Amino Acids in GPCR 138", "position of amino acid")

    sliding_list_10 = give_sliding_hydropathy_value(pure_sequence, mapping_dict, 10)
    print(sliding_list_10)
    plot_hydropathy(sliding_list_10, xvalues, "Average Hydropathy Index in GPCR 138 with Sliding Window Size 10",
                    "starting position of sliding window")

    sliding_list_5 = give_sliding_hydropathy_value(pure_sequence, mapping_dict, 5)
    plot_hydropathy(sliding_list_5, xvalues, "Average Hydropathy Index in GPCR 138 with Sliding Window Size 5",
                    "starting positon of sliding window")

