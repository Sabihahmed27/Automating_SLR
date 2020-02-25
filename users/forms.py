from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Profile, Document, ResearchPapers
import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


# class DataRetrieval(forms.Form):
#     name = forms.CharField()
#     url = forms.URLField()
#     comment = forms.CharField(widget=forms.Textarea)
#     fields = ['Query Data']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description', 'document']

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class SimpleForm(forms.ModelForm):
     Title = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",required=True)
     StartYear = forms.IntegerField(min_value=1960, max_value=current_year(), help_text="Year format: YYYY",required=False ,validators=[MinValueValidator(1960), max_value_current_year])

     EndYear = forms.IntegerField(min_value=1960, max_value=current_year(), help_text="Year format: YYYY", required=False,validators=[MinValueValidator(1960), max_value_current_year])

     Author = forms.CharField(max_length = 200, help_text="Enter Author Name",required=False)


     class Meta:
         model = ResearchPapers
         fields = ['Title', 'Author','StartYear','EndYear']

    #lastname = forms.CharField(max_length=100)


class QueryForm(forms.ModelForm):
    enterUrl = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['enterUrl']

