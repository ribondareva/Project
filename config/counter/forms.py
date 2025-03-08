from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField()


class WordCountForm(forms.Form):
    word = forms.CharField(max_length=100)
