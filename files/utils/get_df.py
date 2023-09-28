"""Gets dataframe from csv"""
import pandas as pd


def get_df(path, usecols=lambda x: x):
    """Handles oversized files too"""

    chunksize = 100000
    # TextFileReader object
    tfr = pd.read_csv(
        path,
        chunksize=chunksize,
        usecols=usecols,
        iterator=True
    )
    # chunks are being concatenated here
    df = pd.concat(tfr, ignore_index=True)

    return df
