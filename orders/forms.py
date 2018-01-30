from django import forms
from .models import *


class CheckForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    adres = forms.CharField(required=True)