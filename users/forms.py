from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from upload_validator import FileTypeValidator
from .models import Profile, Document, ResearchPapers, Articles, Papers, Question, ResearchQuestion, \
    QualityAssessmentQuestions
import datetime
from django.forms import formset_factory,modelformset_factory


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['username', 'email']

class BookForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': 'True',
            'class': 'form-control',
            'placeholder': 'Enter Research Question here'
        })
    )


class QuestionForm(forms.Form):
    question = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': 'True',
            'class': 'form-control',
            'placeholder': 'Enter Research Question here'
        })
    )

BookFormset = formset_factory(BookForm, extra=1)

alphanumeric = RegexValidator(r'^[a-zA-Z0-9\.\s]+$', 'Only alphanumeric characters are allowed.')
QualityModelFormset = modelformset_factory(
    QualityAssessmentQuestions,
    fields=('quality_question',),
    extra=1,
    widgets={'quality_question': forms.TextInput(attrs={
        'required': 'True',
        'class': 'form-control',
        'placeholder': 'Enter your Quality Assessment question here'
    })
    }
)

ResearchFormset = formset_factory(QuestionForm)
ResearchQuestionModelFormset = modelformset_factory(
    ResearchQuestion,
    fields=('question', ),
    extra=1,
    widgets={'question': forms.TextInput(attrs={
            'required': 'True',
            'class': 'form-control',
            'placeholder': 'Enter your question here'
        })
    }
)

class QuestionForm(forms.Form):
    alphanumeric = RegexValidator(r'^[a-zA-Z0-9\.\s]+$', 'Only alphanumeric characters are allowed.')
    quality_question = forms.CharField(
        label='Question',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Question here here'
        }),
        validators=[alphanumeric]

    )
QuestionFormset = formset_factory(QuestionForm, extra=1)


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



class JournalForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[a-zA-Z0-9\.\s]+$', 'Only alphanumeric characters are allowed.')
    title = forms.CharField(max_length=300,help_text="Enter Title",validators=[alphanumeric], required=True)
    author = forms.CharField(max_length = 200, help_text="Enter Author name", validators=[alphanumeric], required=True)
    start_year = forms.IntegerField(min_value=1960, label="Start Year", max_value=current_year(),help_text="Year format: YYYY", required=True,validators=[MinValueValidator(1960), max_value_current_year])
    end_year = forms.IntegerField(min_value=1960, label="End Year", max_value=current_year(),help_text="Year format: YYYY", required=True,validators=[MinValueValidator(1960), max_value_current_year])
    pdf = forms.FileField(label='', help_text="Formats accepted: PDF", required=True,validators=[FileTypeValidator(allowed_types=['application/pdf'])])

    class Meta:
        model = Papers
        fields = ('title', 'author','start_year','end_year','pdf')


# ^[0-9a-zA-Z]*$  ^[a-zA-Z0-9 .!?"-\(\)]+$ ^[a-zA-Z0-9\n _ .?"-:!()]$
# ^[a-zA-Z0-9 _.,!()+=`,"@$#%*-]+$

# '^[0-9a-zA-Z_ .?"-:!()]+$'
class SimpleForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[a-zA-Z0-9\.\s]+$', 'Only alphanumeric characters are allowed.')
    Title = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric], required=True)
    StartYear = forms.IntegerField(min_value=1960, label="Start Year", max_value=current_year(), help_text="Year format: YYYY",required=True ,validators=[MinValueValidator(1960), max_value_current_year])
    EndYear = forms.IntegerField(min_value=1960, label="End Year",max_value=current_year(), help_text="Year format: YYYY", required=True,validators=[MinValueValidator(1960), max_value_current_year])
    Author = forms.CharField(max_length = 200, help_text="Enter Author name", validators=[alphanumeric], required=True)
    Keyword = forms.CharField(max_length=300, help_text="(Keyword for Abstract Screening)",validators=[alphanumeric],required=True)
    class Meta:
        model = Articles
        fields = ['Title', 'Author','StartYear','EndYear','Keyword']

    #lastname = forms.CharField(max_length=100)

class PICOC(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[a-zA-Z0-9\.\s]+$', 'Only alphanumeric characters are allowed.')
    population = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=True)
    intervention = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=True)
    comparison = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=True)
    outcome = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=True)
    context = forms.CharField(max_length=300,help_text="(Keyword AND keyword)",validators=[alphanumeric],required=True)

    class Meta:
        model = ResearchPapers
        fields = ['population','intervention','comparison','outcome','context']



class QuestionForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_ .?"-:!()]+$',message='Only alphanumeric characters are allowed.')
    question1 = forms.CharField(max_length=300,help_text="Please specify Research Question",validators=[alphanumeric],required=True)
    question2 = forms.CharField(max_length=300,help_text="Please specify Research Question",validators=[alphanumeric],required=True)
    question3 = forms.CharField(max_length=300,help_text="Please specify Research Question",validators=[alphanumeric],required=True)

    class Meta:
        model = Question
        fields = ['question1','question2','question3']



class QueryForm(forms.ModelForm):
    enterUrl = forms.CharField(max_length=100)

    class Meta:
        model = Articles
        fields = ['enterUrl']

class SearchBar(forms.ModelForm):
    search_string = forms.CharField(max_length=255)

    class Meta:
        model = Articles
        fields = ['search_string']
