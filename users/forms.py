from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

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

class AbstractForm(forms.ModelForm):
    Keyword = forms.CharField(max_length=300, help_text="(Keyword for search)", required=True)
    class Meta:
        model = ResearchPapers
        fields = ['Keyword']


# ^[0-9a-zA-Z]*$  ^[a-zA-Z0-9 .!?"-\(\)]+$ ^[a-zA-Z0-9\n _ .?"-:!()]$
# ^[a-zA-Z0-9 _.,!()+=`,"@$#%*-]+$
class SimpleForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_ .?"-:!()]+$', 'Only alphanumeric characters are allowed.')
    Title = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=True)
    StartYear = forms.IntegerField(min_value=1960, label="Start Year", max_value=current_year(), help_text="Year format: YYYY",required=True ,validators=[MinValueValidator(1960), max_value_current_year])
    EndYear = forms.IntegerField(min_value=1960, label="End Year",max_value=current_year(), help_text="Year format: YYYY", required=True,validators=[MinValueValidator(1960), max_value_current_year])
    Author = forms.CharField(max_length = 200, help_text="Enter Author name",required=True)
    Keyword = forms.CharField(max_length=300, help_text="(Keyword for Abstract Screening)", required=True)
    class Meta:
        model = ResearchPapers
        fields = ['Title', 'Author','StartYear','EndYear','Keyword']

    #lastname = forms.CharField(max_length=100)

class PICOC(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_ .?"-:!()]+$', 'Only alphanumeric characters are allowed.')
    population = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=False)
    intervention = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=False)
    comparison = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=False)
    outcome = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=False)
    context = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=False)

    class Meta:
        model = ResearchPapers
        fields = ['population','intervention','comparison','outcome','context']



class QueryForm(forms.ModelForm):
    enterUrl = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['enterUrl']

