from django import forms

class URLForm(forms.Form):
    url = forms.CharField(max_length=1000)

class TagForm(forms.Form):
    title = forms.CharField(max_length=100)
    element = forms.CharField(max_length=100)
    attribute = forms.CharField(max_length=100)
    value = forms.CharField(max_length=100)

class NavURLForm(forms.Form):
    navtitle = forms.CharField(max_length=100)
    navelement = forms.CharField(max_length=100)
    navattribute = forms.CharField(max_length=100)
    navvalue = forms.CharField(max_length=10000)

class DataForm(forms.Form):
    radio = (
        ('10', '10'),
        ('20', '20'),
        ('30', '30'),
    )
    select = [
        ('csv', '.csv'),
        ('json', '.json'),
    ]
    raw = [
        ('true', 'raw'),
        ('false', 'processed'),
    ]
    page = forms.ChoiceField(choices=radio, widget=forms.Select(attrs={'class': 'form-control'}))
    raw = forms.ChoiceField(widget=forms.RadioSelect, choices=raw)
    format = forms.ChoiceField(widget=forms.RadioSelect, choices=select)

