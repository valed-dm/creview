"""Contains files app tables schemas"""

import django_tables2 as tables

from files.models import File


class FilesTable(tables.Table):
    """Creates uploaded files table to be presented by view"""

    file = tables.FileColumn(attrs={
        "td": {"class": "bg-success"},
        "a": {"style": "color: white;"},
    })
    delete = tables.CheckBoxColumn(accessor='pk')

    class Meta:
        """Metadata for FilesTable"""

        model = File
        fields = ['file', 'date', 'status']
