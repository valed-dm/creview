"""File upload form"""
from django import forms


class UploadFileForm(forms.Form):
    """Provides file upload"""

    file = forms.FileField(label='', help_text='NOTE: only .csv files allowed!')
