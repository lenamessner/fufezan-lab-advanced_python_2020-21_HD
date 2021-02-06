import csv
from collections import Counter, OrderedDict
from matplotlib import pyplot as plt


def extract_sequence(fastafile):
    with open(dataset) as fastafile:
        all_sequences = ""
        for row in fastafile:
            if not row[0] == ">":
                all_sequences += row.replace("\n", "")  # .replace, damit all_sequences alles in einer Zeile
    return all_sequences


def results_as_csv(ordered_dict=None, name_of_organism=""):
    if ordered_dict is None:
        ordered_dict = {}
    with open("results_exercice2/csv__orderd.csv", "w") as output:
        csv_writer = csv.DictWriter(output, fieldnames=["aa", "count"], delimiter=",")
        csv_writer.writeheader()
        for key, value in ordered_dict.items():
            csv_writer.writerow({'aa': key, 'count': value})
    print(ordered_dict)


def plot_results(ordered_dict=None, name_of_organism=""):
    if ordered_dict is None:
        ordered_dict = {}
    as_names = []  # geht auch einfach als list(counter_dict.keys())
    for key in ordered_dict.keys():
        as_names += key
    # print(as_names)

    as_count = []
    for value in ordered_dict.values():
        as_count += [value]  # as_count.append(value) geht, += braucht gleichen Datentyp
    # print(as_count)

    plt.bar(as_names, as_count, color='darkred')
    plt.ylabel("counts")
    plt.xlabel("amino acid")
    plt.title(f"Histogram of amino acids in {name_of_organism}")
    plt.show()
    # plt.savefig("results_exercice2/hist_{name_of_organism}_messner_ordered.pdf")


if __name__ == '__main__':
    dataset = "data_exercice2/uniprot-archae+AND+reviewed_yes+AND+Methanococcus+maripaludis.fasta"
    all_sequences = extract_sequence(dataset)

    counter_dict = dict(Counter(all_sequences))
    ordered_dict = OrderedDict(sorted(dict.items(Counter(all_sequences))))

    print(type(sorted(dict.items(Counter(all_sequences)))))  # out: list
    # könnte also vermutlich auch direkt das benutzen...

    # for key, value in counter_dict.items():
    #     print(key)
    #     print(value)
    # gibt abwechselnd Buchstabe und Zahl -> wie erwartet

    plot_results(ordered_dict, "mmaripaludis")

    with open("results_exercice2/csv_mmaripaludis_ordered.csv", "w") as output:
        csv_writer = csv.DictWriter(output, fieldnames=["aa", "count"], delimiter=",")
        csv_writer.writeheader()
        for key, value in ordered_dict.items():
            csv_writer.writerow({'aa': key, 'count': value})