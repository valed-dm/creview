"""Contains files app tables schemas"""

import django_tables2 as tables

from files.models import File


class CheckBoxColumnWithName(tables.CheckBoxColumn):
    """Overrides default CheckBoxColumn"""

    @property
    def header(self):
        return self.verbose_name


class FilesTable(tables.Table):
    """Creates uploaded files table to be presented by view"""

    file = tables.FileColumn(attrs={
        "td": {"class": "bg-success"},
        "a": {"style": "color: white;"},
    })
    delete = CheckBoxColumnWithName(
        verbose_name="Delete Files",
        accessor='pk',
        attrs={
            "th": {"class": "text-danger"},
            "input": {"style": "height: 13px"}
        }
    )

    class Meta:
        """Metadata for FilesTable"""

        model = File
        fields = ['file', 'date', 'status']
