# forms.py
from django import forms
from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['schedule_name','schedule_query_id','date', 'time', 'utc', 'schedule_name', 'query']
class IPDetailsForm(forms.Form):
    ipadress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'IPAdress'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    query_id = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Query'}))


