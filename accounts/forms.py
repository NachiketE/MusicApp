# In your forms.py

from django import forms

class MusicForm(forms.Form):
    title = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=100)
    genre = forms.CharField(max_length=50)
    duration = forms.CharField(max_length=10)
    release_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    trendy = forms.BooleanField(required=False, label='Trendy')
    def clean_trendy(self):
        trendy = self.cleaned_data['trendy']
        return '1' if trendy else '0'