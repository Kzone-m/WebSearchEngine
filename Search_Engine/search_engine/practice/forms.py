from django import forms
from .models import BaseballPlayer #, Team


NAME_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your name -> ex: Taro Tanaka'}
YEARLY_PAY_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your yearly pay'}
YEARLY_PAY_MAX_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'enter maximum yearly pay'}
YEARLY_PAY_MIN_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'enter minimum yearly pay'}
POSITION_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your position'}
TEAM_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter your team'}


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


class BaseballPlayerSearchForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs= NAME_ATTRIBUTE), required=False)
    yearly_pay_min = forms.IntegerField(min_value=1, label='', widget=forms.NumberInput(attrs=YEARLY_PAY_MIN_ATTRIBUTE), required=False)
    yearly_pay_max = forms.IntegerField(min_value=1, label='', widget=forms.NumberInput(attrs=YEARLY_PAY_MAX_ATTRIBUTE), required=False)
    position = forms.CharField(label='', widget=forms.TextInput(attrs= POSITION_ATTRIBUTE), required=False)
    team = forms.CharField(label='', widget=forms.TextInput(attrs= TEAM_ATTRIBUTE), required=False)

    class Meta:
        model = BaseballPlayer
        fields = ('name', 'position', 'team')

    def filter_players(self, players):
        if self.is_valid():
            name = self.cleaned_data.get('name')
            yearly_pay_min = self.cleaned_data.get('yearly_pay_min')
            yearly_pay_max = self.cleaned_data.get('yearly_pay_max')
            position = self.cleaned_data.get('position')
            team = self.cleaned_data.get('team')

            if name:
                players = players.filter(name__contains=name)
            if yearly_pay_min:
                players = players.filter(yearly_pay__gte=yearly_pay_min)
            if yearly_pay_max:
                players = players.filter(yearly_pay__lte=yearly_pay_max)
            if position:
                players = players.filter(position=position)
            if team:
                players = players.filter(team=team)
            return players
        else:
            return players

