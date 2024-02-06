from django import forms
from . models import Regular_Schedule

class WeekForm(forms.Form):
    week = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    

    



    


