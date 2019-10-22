from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


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

class SimpleForm(forms.Form):
     enterUrl = forms.CharField(max_length=100)


     class Meta:
         model = forms
         fields = ['query']
    #lastname = forms.CharField(max_length=100)


class QueryForm(forms.Form):
    query = forms.CharField(max_length=100)
