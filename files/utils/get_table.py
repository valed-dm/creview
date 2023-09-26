"""
Dynamically creates class for .csv file preview in a browser
as django_tables2 table on the base of a csv header's list
"""
import django_tables2 as tables


def get_table_from_headers(headers: list) -> type:
    """Creates CSVTable class from a list of .csv file headers"""

    attrs = {}
    for item in headers:
        if item.lower() in ["links", "image"]:
            # creates columns with clickable external links
            attrs[str(item)] = tables.URLColumn(
                attrs={"a": {"style": "color: white;"}},
            )
        else:
            attrs[str(item)] = tables.Column()

    # returns dynamically created django_tables2 CSVTable class
    return type("CSVTable", (tables.Table,), attrs)
