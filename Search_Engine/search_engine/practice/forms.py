from django import forms
from .models import BaseballPlayer #, Team

NAME_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your name -> ex: Taro Tanaka'}
YEARLY_PAY_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your yearly pay'}
POSITION_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your position'}
TEAM_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your team'}

'''
POSITION = (
    ('Pitcher', 'pitcher'),
    ('Catcher', 'catcher'),
    ('Infielder', 'infielder'),
    ('Outfielder', 'outfielder')
)
'''


class BaseballPlayerAddForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs= NAME_ATTRIBUTE))
    yearly_pay = forms.IntegerField(min_value=1, label='', widget=forms.NumberInput(attrs=YEARLY_PAY_ATTRIBUTE))
    position = forms.CharField(label='', widget=forms.TextInput(attrs= POSITION_ATTRIBUTE))
    team = forms.CharField(label='', widget=forms.TextInput(attrs= TEAM_ATTRIBUTE))
    # position = forms.ChoiceField(label='', choices= POSITION, widget=forms.Select(attrs=POSITION_ATTRIBUTE))
    # team = forms.ModelChoiceField(label='', queryset=Team.objects.all(), widget=forms.Select(attrs=TEAM_ATTRIBUTE))

    class Meta:
        model = BaseballPlayer
        fields = ('name', 'yearly_pay', 'position', 'team')