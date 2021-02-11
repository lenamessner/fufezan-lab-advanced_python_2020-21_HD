import numpy as np
import pandas as pd
import timeit


def msp_to_df(
        input_file,
        max_seq_len=30,
        min_ce=36,
        max_ce=40,
        mz_min=135,
        mz_max=1400,
):
    """
    Function to read spectrum data from .msp file and convert to dataframe.
    Args:
        input_file (str): path to .msp file
        max_seq_len (int): maximum acceptable sequence length
        min_ce (int): minimum collision energy of spectra to be included in df
        max_ce (int): maximum collision energy of spectra to be included in df
        mz_min (int): lower boundary for m/z to be included in df
        mz_max (int): lower boundary for m/z to be included in df

    Returns:
        df (pd.DataFrame or np.array): spectrum information within defined parameters [n_spectra, n_features]
        seqs (pd.DataFrame or np.array): sequences
    """
    with open(input_file) as mspfile:
        mspfile = mspfile.read()

        # split mspfile in different measurements
        list_of_spectra = mspfile.split("\n\n")
        list_of_spectra = list_of_spectra[:-1]  # um die letzte, leere Sequenz rauszulassen
        # print(len(list_of_spectra), list_of_spectra[0])  # out: 17852, erste Messung

    # selection of sequences
    seqs = np.empty((0, 2))
    dict = {}
    for whichspectrum, spectrum in enumerate(list_of_spectra):
        # extract collision energy
        row_split = spectrum.split("\n")
        ce_row = row_split[0]
        ce_part = ce_row.split("_")
        ce = float(ce_part[-1][:-2])
        # print(ce)

        if min_ce <= ce <= max_ce:  # only continue if ce is in range
            seq_split = spectrum.split("/")
            seq_part = seq_split[0]
            seq = seq_part[6:]
            seq_length = len(seq)

            if seq_length <= max_seq_len:  # only continue if seq_length is in range
                seqs = np.append(seqs, [[whichspectrum, seq]], axis=0)

                # extract intensity values
                dict[whichspectrum] = {}
                for m, row in enumerate(row_split):
                    if not row[0] == "N" and not row[0] == "M" and not row[0] == "C":
                        data_split = row.split("\t")
                        mz_ratio = round(float(data_split[0]))
                        intensity = float(data_split[1])
                        if mz_min <= mz_ratio <= mz_max:  # only continue if mz_ration is in range
                            if mz_ratio in dict[whichspectrum].keys():
                                if intensity > dict[whichspectrum][mz_ratio]:
                                    dict[whichspectrum][mz_ratio] = intensity
                            else:
                                dict[whichspectrum][mz_ratio] = intensity
    df = pd.DataFrame(dict).sort_index()
    df = df.T
    df.dropna(how="all", inplace=True)
    df.fillna(0, inplace=True)
    # print(df.head())

    seqs = pd.DataFrame(seqs).set_index(0)
    seqs.rename(columns={1: "sequence"}, inplace=True)

    return df, seqs


if __name__ == '__main__':
    input_file = "../data/cptac2_mouse_hcd_selected.msp"
    result = msp_to_df(input_file)
    print("dataframe= \n", result[0].head())
    print("seqs: \n", result[1].head())
