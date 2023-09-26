"""Files app tables schemas"""
import django_tables2 as tables
from django_tables2.columns.base import LinkTransform

from files.models import File
from files.utils.get_attrs import get_attrs

LinkTransform.get_attrs = get_attrs


class CheckBoxColumnWithName(tables.CheckBoxColumn):
    """Overrides default CheckBoxColumn header"""

    @property
    def header(self):
        """Assigns a name (verbose_name="Delete") to column header"""

        return self.verbose_name


class FilesTable(tables.Table):
    """Creates uploaded files table to be presented by view"""

    file = tables.FileColumn(attrs={
        "td": {"class": "bg-success"},
        "a": {"style": "color: white;"},
    })
    delete = CheckBoxColumnWithName(
        verbose_name="Delete",
        accessor='pk',
        attrs={
            "th": {"class": "text-danger"},
            "input": {"style": "height: 13px"}
        }
    )

    class Meta:
        """Metadata for FilesTable"""

        model = File
        fields = ['file', 'headers', 'date', 'status', 'size']
