from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='选择文件',
        help_text='max. 42 megabytes'
    )
