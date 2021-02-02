import csv
from collections import Counter, OrderedDict
from matplotlib import pyplot as plt


with open("../data/uniprot-filtered-organism__Homo+sapiens.fasta") as fastafile:
    all_sequences = ""
    for row in fastafile:
        if not row[0] == ">":
            all_sequences += row.replace("\n", "")  #.replace, damit all_sequences alles in einer Zeile

counter_dict = dict(Counter(all_sequences))
ordered_dict = OrderedDict(sorted(dict.items(Counter(all_sequences))))

print(type(sorted(dict.items(Counter(all_sequences)))))  # out: list
# könnte also vermutlich auch direkt das benutzen...

# for key, value in counter_dict.items():
#     print(key)
#     print(value)
    # gibt abwechselnd Buchstabe und Zahl -> wie erwartet

with open("../results/human.csv", "w") as output:
    csv_writer = csv.DictWriter(output, fieldnames=["aa", "count"], delimiter=",")
    csv_writer.writeheader()
    for key, value in counter_dict.items():
        csv_writer.writerow({'aa': key, 'count': value})

as_names = []   # geht auch einfach als list(counter_dict.keys())
for key in ordered_dict.keys():
    as_names += key
print(as_names)

as_count = []
for value in ordered_dict.values():
    as_count += [value]    # as_count.append(value) geht, += braucht gleichen Datentyp
print(as_count)


plt.bar(as_names, as_count, color='darkred')
plt.ylabel("counts")
plt.xlabel("amino acid")
plt.title("Histogram of amino acids in Homo sapiens")
# plt.show()
# plt.savefig("../results/hist_human_messner_ordered.pdf")
