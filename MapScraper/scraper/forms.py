from django import forms

class SearchForm(forms.Form):
    consulta = forms.CharField(label="Qué quieres buscar", max_length=100)
    ciudad = forms.CharField(label="Ciudad", max_length=100)
