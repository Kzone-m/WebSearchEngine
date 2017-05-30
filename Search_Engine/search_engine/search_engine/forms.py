from django import forms

SEED_URL_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter Seed URL: e.x. https://www.yahoo.co.jp'}
MAX_DEPTH_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter Maximum Depth: e.x. 2'}
MAX_CAPACITY_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter Maximum Capacity: e.x. 100'}
TARGET_HTML_TAG_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter Target HTML Tag: e.x. h1'}
QUERY_ATTRIBUTE = {'class': 'form-control', 'placeholder': 'Enter Seed URL: e.x. やきいも'}


class ScrapingForm(forms.Form):
    seed_url = forms.CharField(label='', widget=forms.TextInput(attrs=SEED_URL_ATTRIBUTE))
    max_depth = forms.IntegerField(label='', min_value=0, widget=forms.NumberInput(attrs=MAX_DEPTH_ATTRIBUTE))
    max_capacity = forms.IntegerField(label='', min_value=0, widget=forms.NumberInput(attrs=MAX_DEPTH_ATTRIBUTE))
    target_html_tag = forms.CharField(label='', widget=forms.TextInput(attrs=TARGET_HTML_TAG_ATTRIBUTE))


class LookUpForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs=QUERY_ATTRIBUTE))
