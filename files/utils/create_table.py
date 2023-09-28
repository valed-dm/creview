"""
Dynamically creates class for .csv file preview in a browser
as django_tables2 table on the base of a csv header's list
"""
import django_tables2 as tables

from files.tables import CheckBoxColumnWithName


def create_table_from_headers(headers: list, links: list) -> type:
    """Creates CSVTable class from a list of .csv file headers"""

    attrs = {}

    if links is None:
        links = []

    for item in headers:
        if item in links:
            # columns with clickable external links
            attrs[str(item)] = tables.URLColumn(
                attrs={"a": {"style": "color: white;"}},
            )
        elif item in ["include", "as_link"]:
            # checkboxes for table view customization
            attrs[str(item)] = CheckBoxColumnWithName(
                verbose_name=item,
                accessor='columns',
                attrs={
                    "th": {"class": "text-success"},
                    "input": {"style": "height: 13px"}
                },
                empty_values=()
            )
        else:
            # text columns
            attrs[str(item)] = tables.Column()

    # returns dynamically created django_tables2 CSVTable class
    return type("CSVTable", (tables.Table,), attrs)
