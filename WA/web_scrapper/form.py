from django import forms

class URLForm(forms.Form):
    url = forms.CharField(max_length=1000)

class TagForm(forms.Form):
    title = forms.CharField(max_length=100)
    element = forms.CharField(max_length=100)
    attribute = forms.CharField(max_length=100)
    value = forms.CharField(max_length=100)

class NavURLForm(forms.Form):
    navtitle = forms.CharField(max_length=100, label="Title")
    navelement = forms.CharField(max_length=100, label="Element")
    navattribute = forms.CharField(max_length=100, label="Attribute")
    navvalue = forms.CharField(max_length=10000, label="Value")

class DataForm(forms.Form):
    page = forms.IntegerField(label='Pages', required=False)


