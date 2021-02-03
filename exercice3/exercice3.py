import pandas as pd
import plotly.graph_objects as go

aap = "../data/amino_acid_properties.csv"

genseq = "GP183_human.fasta"

# create mapping_dict from csv-file with aap
aap_df = pd.read_csv(aap)
mapping_dict = {}
for aa in range(len(aap_df.index)):
    for hydroind in range(len(aap_df.index)):
        mapping_dict[str(aap_df.loc[aa, '1-letter code'])] = aap_df.loc[aa, 'hydropathy index (Kyte-Doolittle method)']
print(mapping_dict)

# extract sequence from fasta as string
with open(genseq) as genseq_fasta:
    pure_sequence = ""
    for row in genseq_fasta:
        if not row[0] == ">":
            pure_sequence += row.replace("\n", "")
print(pure_sequence)


# return hydropathy values according to sequence
def give_hydropathy_value(sequence="", mapping_dict={}):
    hydropathy_values = []
    for aa in pure_sequence[:]:
        hydropathy_values.append(mapping_dict[str(aa)])
    return (hydropathy_values)

hydropathy_list = give_hydropathy_value(pure_sequence, mapping_dict)
# print(hydropathy_values)

# plot hydropathy list

data = [
    go.Bar(
        x=aap_df["1-letter code"],
        y=hydropathy_list
    )
]

fig = go.Figure(data=data)
fig.update_layout(template="plotly_dark", title="AA hydropathy index")
fig.show()
# if __name__ == '__main__':
#     hydropathy_values = give_hydropathy_value(pure_sequence, mapping_dict)
#     print(hydropathy_values)
