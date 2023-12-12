# forms.py
from django import forms

class IPDetailsForm(forms.Form):
    ipadress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'IPAdress'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    query_id = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Query'}))
    
class ScheduleForm(forms.Form):
    schedule_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    schedule_query_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Query No'}))
    schedule_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Data'}))
    schedule_query_id = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Query No'}))

