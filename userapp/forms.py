from django import forms
from movieapp.models import MovieDetails

class MovieForm(forms.ModelForm):
    class Meta:
        model=MovieDetails
        fields=['title','description','actors','poster','release_date','trailer_Link']