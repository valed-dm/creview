from files.utils.bool_switch import switch


def df_sort(df, sort):
    df = df.sort_values(by=[sort], ascending=switch.switch())
    return df
