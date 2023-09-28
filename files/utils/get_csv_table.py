"""Creates paginated tables from df"""
from files.utils.create_table import create_table_from_headers


def get_csv_table(request, df, links):
    """Paginated table is ready to be rendered"""

    headers = []
    for col in df.columns:
        headers.append(col)
    # dynamically created django_tables2 CSVTable class
    dynamic_table = create_table_from_headers(headers, links)
    table = dynamic_table(
        data=df.to_dict("records"),
        template_name="django_tables2/bootstrap5.html"
    )
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    return table
