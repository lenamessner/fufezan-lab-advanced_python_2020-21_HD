import csv
from collections import Counter
from matplotlib import pyplot as plt


with open("../data/uniprot-archae+AND+reviewed_yes+AND+Methanococcus+maripaludis.fasta") as fastafile:
    all_sequences = ""
    for row in fastafile:
        if not row[0] == ">":
            all_sequences += row.replace("\n", "")  #.replace, damit all_sequences alles in einer Zeile

counter_dict = dict(Counter(all_sequences))
print(counter_dict.keys())
print(counter_dict.values())

# with open("../human.csv", "w") as output:
#     aap_writer = csv.DictWriter(output, fieldnames=["aa", "count"])
#     aap_writer.writeheader()
#     for key, value in counter_dict.items():
#         aap_writer.writerow({key: value})

as_names = []
for key in counter_dict.keys():
    as_names += key
print(as_names)

as_count = []
for value in counter_dict.values():
    as_count += [value]    # as_count.append(value) geht, += braucht gleichen Datentyp
print(as_count)


plt.bar(as_names, as_count, color='darkred')
plt.ylabel("counts")
plt.xlabel("amino acid")
plt.title("Histogram of amino acids in Methanococcus maripaludis")
# plt.show()
plt.savefig("../results/hist_mmaripaludis_messner.pdf")

# with open("../test.csv", "w") as output:
#     aap_writer = csv.DictWriter(output, fieldnames=["Name", "3-letter code"], extrasaction="ignore")
#     aap_writer.writeheader()
#     aap_writer.writerow({"Name": "Alanine", "3-letter code": "Ala", "1-letter code": "A"})
