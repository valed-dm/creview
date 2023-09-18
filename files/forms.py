from django import forms


class UploadFileForm(forms.Form):
    # category = forms.ChoiceField(get_category_list())
    file = forms.FileField(label='', help_text='NOTE: only .py files allowed!')
