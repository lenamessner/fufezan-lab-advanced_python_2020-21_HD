import pandas as pd
import requests
import plotly.graph_objects as go


class Protein:
    """
    class representing proteins
    """

    def __init__(self, id, lookup):
        """
        initializing instances for the Protein class
        Args:
            id: id of the protein
            lookup: dict containing properties of the aa e.g.{"hydropathy": {"A": }}
        """

        self.id = id
        self.lookup = lookup
        self.sequence = None

    def get_data(self):
        """
        pulls fasta from uniprot using the id, then extracts sequence
        Args:
            id: id of the protein

        Returns:
            sequence: sequence of the protein as string

        """

        url = f"https://www.uniprot.org/uniprot/{self.id}.fasta?fil=reviewed:yes"
        r = requests.get(url)
        protein_csv = f"{self.id}.fasta"
        with open(protein_csv, 'wb') as fasta:
            fasta.write(r.content)
        with open(protein_csv) as genseq_fasta:
            sequence = ""
            for row in genseq_fasta:
                if not row[0] == ">":
                    sequence += row.replace("\n", "")
        return sequence

    def map(self, which_lookup="", window_size=1):
        """
        maps the sequence against a given aa property using the average value of a given number of aa
        Args:
            which_lookup: string, which aa property should be looked at
            window_size: size of sliding window as int

        Returns:
            requested_values: list of aa properties according to sequence

        """

        requested_values_average = []
        for pos, aa in enumerate(self.sequence):
            if pos > len(self.sequence)-window_size:
                break
            values = 0
            for subseq_aa in self.sequence[pos:pos+window_size]:
                values += self.lookup[which_lookup][str(subseq_aa)]
            average_value = values/window_size
            requested_values_average.append(average_value)
        return requested_values_average


def plot_values(value_list=None, seq="", title=""):
    """
    plots hydropathy values against given x values using plotly
    Args:
        value_list: list containing y-values to be plotted
        seq: aa seq to be iterated
        title: title of plot as string

    Returns:
        required plot

    """

    if value_list is None:
        value_list = []
    data = [
        go.Bar(
            x=list(range(len(seq))),
            y=value_list,
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
                "text": "starting position of sliding window",
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

def get_lookup_dict(aap_df):
    """

    Args:
        aap_df: panda df with aa properties

    Returns: lookup_dict: dict that contains properties as first keys, then aa as second key, then corresponding
                values, e.g.: {"hydropathy": {{"A": 1.2}, {"C": 2.2},...}, "pI":{...} }

    """

    lookup_dict = {}
    for property in aap_df.columns:
        lookup_dict[property] = {}
        for aa in range(len(aap_df.index)):
            lookup_dict[property][str(aap_df.loc[aa, '1-letter code'])] = aap_df.loc[aa, property]
    return lookup_dict


if __name__ == '__main__':

    aap_df = pd.read_csv("../data/amino_acid_properties.csv")
    aap_df = aap_df.rename(
        columns={"hydropathy index (Kyte-Doolittle method)": "hydropathy index"})  # .rename ändert Var ned!
    lookup_dict = get_lookup_dict(aap_df)
    print(lookup_dict)
    GPCR183 = Protein(id="P32249", lookup=lookup_dict)
    GPCR183.sequence = GPCR183.get_data()
    hydropathy_values = GPCR183.map("hydropathy index", 10)
    residue_weight = GPCR183.map("Residue Weight", 5)
    print(residue_weight)
    print(hydropathy_values)

    plot_values(value_list=hydropathy_values, seq=GPCR183.sequence,
                title="hydropathy values of GPCR183 with window size 10")
    plot_values(residue_weight, seq=GPCR183.sequence,
                title="residue values of GPCR183 with window size 3")
