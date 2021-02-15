import pandas as pd
import plotly.graph_objects as go


# create mapping_dict from csv-file with aap
def create_mapping_dict(csv_file=""):
    """
    creates a dict that maps aa-1-letter-code to corresponding hydropathy index
    :param csv_file: string with path for csv_file that contains aa properties
    :return: dict that contains aa name as key and hydropathy as value
    """
    aap_df = pd.read_csv(csv_file)
    mapping_dict = {}
    for aa in range(len(aap_df.index)):
        for hydroind in range(len(aap_df.index)):
            mapping_dict[str(aap_df.loc[aa, '1-letter code'])] = aap_df.loc[
                aa, 'hydropathy index (Kyte-Doolittle method)']
    return mapping_dict


# extract sequence from fasta as string
def extract_sequence(fasta):
    """
    extracts pure sequence from fastafile
    :param fasta: fasta file that contains sequence
    :return: pure sequence as string (one line, without header)
    """
    with open(fasta) as genseq_fasta:
        pure_sequence = ""
        for row in genseq_fasta:
            if not row[0] == ">":
                pure_sequence += row.replace("\n", "")
    return pure_sequence


# return hydropathy values according to sequence
def give_hydropathy_value(pure_sequence="", mapping_dict=None):
    """
    turns sequence into hydropathy values
    :param pure_sequence: sequence to be analysed as string
    :param mapping_dict: dict that maps aa to corresponding hydropathy index
    :return: list that contains hydropathy values of sequence
    """
    if mapping_dict is None:
        mapping_dict={}
    hydropathy_values = []
    for aa in pure_sequence[:]:
        hydropathy_values.append(mapping_dict[str(aa)])
    return hydropathy_values


# plot hydropathy list
def plot_hydropathy(hydropathy_list=None, xvalues=None, title="", xtitle=""):
    """
    plots hydropathy values against given x values using plotly
    :param hydropathy_list: list containing hydropathy indices
    :param xvalues: list containing aa position
    :param title: title of plot as string
    :param xtitle: title of x-axis as string
    :return: required plot
    """
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
def give_sliding_hydropathy_value(pure_sequence="", mapping_dict=None, window_size=1):
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

    genseq_fasta = "GP183_human.fasta"

    mapping_dict = create_mapping_dict(aap)
    print(mapping_dict)

    pure_sequence = extract_sequence(genseq_fasta)
    print(pure_sequence)

    xvalues=[]
    for pos in range(len(pure_sequence)):
        xvalues.append(pos)
    print(xvalues)

    hydropathy_values = give_hydropathy_value(pure_sequence, mapping_dict)
    print(hydropathy_values)
    plot_hydropathy(hydropathy_values, xvalues, "Hydropathy Index of Amino Acids in GPCR 183", "position of amino acid")

    sliding_list_10 = give_sliding_hydropathy_value(pure_sequence, mapping_dict, 10)
    print(sliding_list_10)
    plot_hydropathy(sliding_list_10, xvalues, "Average Hydropathy Index in GPCR 183 with Sliding Window Size 10",
                    "starting position of sliding window")

    sliding_list_5 = give_sliding_hydropathy_value(pure_sequence, mapping_dict, 5)
    plot_hydropathy(sliding_list_5, xvalues, "Average Hydropathy Index in GPCR 183 with Sliding Window Size 5",
                    "starting positon of sliding window")

