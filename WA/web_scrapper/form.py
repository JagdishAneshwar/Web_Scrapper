from django import forms

class URLForm(forms.Form):
    url = forms.CharField(max_length=1000)

class TagForm(forms.Form):
    title = forms.CharField(max_length=100)
    element = forms.CharField(max_length=100)
    attribute = forms.CharField(max_length=100)
    value = forms.CharField(max_length=100)
