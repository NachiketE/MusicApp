# In your forms.py

from django import forms

class MusicForm(forms.Form):
    title = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=100)
    genre = forms.CharField(max_length=50)
    duration = forms.CharField(max_length=10)
    release_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
