from files.handlers.filter_by_rows_values import filter_by_rows_values
from files.utils.float_or_int_or_bool import float_or_int_or_bool
from files.utils.get_df import get_df


def handle_filter_by_rows(request, path, sort, form):
    """Filters by single column's multiple row values"""

    filter_data = {}
    customized_path = request.session["customized_path"]

    df = get_df(path=path, sort=sort)

    if form.is_valid() and request.method == "POST":

        column = request.POST.get("column") or None
        rows = request.POST.get("rows") or None
        exclude = request.POST.get("rows_exclude") or False
        rows_tuple = tuple(
            map(
                lambda s: float_or_int_or_bool(s.strip()), rows.split(',')
            )
        )
        # filtering data dictionary
        column = column.lower().replace(" ", "_")
        filter_data[column] = rows_tuple

        print(filter_data)

        df = filter_by_rows_values(
            val_dict=filter_data,
            dataframe=df,
            not_include=(True if exclude == "on" else exclude)
        )
        df.to_csv(customized_path, index=False, encoding='utf-8')

        return False,

    return True, df
