"""Forms"""
from django import forms


class UploadFileForm(forms.Form):
    """File upload form"""

    file = forms.FileField(
        label="",
        widget=forms.FileInput(
            attrs={
                'accept': ".csv",
                "class": "form-control"
            }
        ),
        help_text=""
    )


class ColumnRowsForm(forms.Form):
    """One column - many rows filter form"""

    column = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'header'}
        )
    )
    rows = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'val1,val2,val3,...'}
        )
    )
    rows_exclude = forms.BooleanField(required=False, initial=False)
