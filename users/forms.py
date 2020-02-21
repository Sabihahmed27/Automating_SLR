from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Document, ResearchPapers


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


class SimpleForm(forms.ModelForm):
     Title = forms.CharField(max_length=300,help_text="(Keyword AND keyword)")


     class Meta:
         model = ResearchPapers
         fields = ['Title']
    #lastname = forms.CharField(max_length=100)


class QueryForm(forms.ModelForm):
    enterUrl = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['enterUrl']

