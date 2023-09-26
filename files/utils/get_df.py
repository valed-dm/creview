"""Gets dataframe from csv"""
import pandas as pd


def get_df(path):
    """Handles oversized files too"""

    chunksize = 100000
    # TextFileReader object
    tfr = pd.read_csv(path, chunksize=chunksize, iterator=True)
    # chunks are being concatenated here
    df = pd.concat(tfr, ignore_index=True)

    return df
