"""
Multiple rows filtering
"""


def filter_by_rows_values(val_dict, dataframe, not_include):
    """Executes multiple row search with one or many column's values"""

    # df columns headers all lowercase
    dataframe.columns = [
        str(x).lower().replace(" ", "_") for x in dataframe.columns
    ]
    # gets column header (key) from dictionary
    key = list(val_dict)[0]
    # replace   to perform dataframe filtering
    df = dataframe.replace(" ", " ", regex=True)

    # .isin() considers multiple column values rows contain
    mask = df[key].isin(val_dict[key])

    # invert mask to exclude rows if requested
    if not_include:
        mask = ~mask

    res = dataframe[mask]

    return res
