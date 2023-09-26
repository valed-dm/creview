"""
Overrides get_attrs method for django_tables2 LinkTransform class
https://django-tables2.readthedocs.io/en/latest/_modules/django_tables2/columns/base.html
https://django-tables2.readthedocs.io/en/latest/_modules/django_tables2/columns/filecolumn.html
to target FileColumn links to csv_table view instead of file reading in the user's media folder

"""
from django_tables2.utils import AttributeDict, computed_values


def get_attrs(self, **kwargs):
    attrs = AttributeDict(computed_values(self.attrs or {}, kwargs=kwargs))
    file_requested = "?f=" + str(self.compose_url(**kwargs)).strip("/")
    attrs["href"] = f"/csv_table/{file_requested}"
    return attrs
