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
        seqs = []
        for row in mspfile:
            if row[:6] == "Name: ":
                seq_length = 0
                for x in range(6, len(row)):
                    if row[x] != "/":
                        seq_length += 1
                    else:
                        break
                print(seq_length)
                if seq_length <= max_seq_len:
                    seqs.append(row[6:6+seq_length])

    df = None
    seqs = seqs

    return df, seqs


# feature = m/z ratio

if __name__ == '__main__':
    input_file = "../data/cptac2_mouse_hcd_selected.msp"
    result = msp_to_df(input_file)
    print(result)
