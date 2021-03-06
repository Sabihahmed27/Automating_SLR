from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
from django.utils import timezone
from django.urls import reverse
from .validators import validate_file

# Create your models here.

class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Title

class DatabaseSearch_Datatable(models.Model):
    Title=models.CharField(max_length=255,blank=True)
    Year = models.IntegerField(blank=True)
    Url = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Title,self.Year,self.Url

    class Meta:
        ordering = ['Title']

        def __unicode__(self):
            return self.title

class Snowballing_model(models.Model):
    Title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.Title


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question1 = models.CharField(max_length=255)
    question2 = models.CharField(max_length=255, null=True)
    question3 = models.CharField(max_length=255, null=True)
    isbn_number = models.CharField(max_length=13)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    isbn_number = models.CharField(max_length=13)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.name

class QualityAssessmentQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    quality_question = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def _str_(self):
        return self.quality_question
# class Snowballing_articles(models.Model):
#     article = models.CharField(max_length=255,blank=True)
#
#     def __str__(self):
#         return self.article
#
# class Journal(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.CharField(max_length=100)
#     pdf = models.FileField(upload_to='documents/')
#
#     def __str__(self):
#         return self.title

class ResearchQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question

class Papers(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_year = models.CharField(blank=True,max_length=100)
    end_year = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)

    def filename(self):
        # return self.pdf.url
        return os.path.basename(self.pdf.url)



class Document(models.Model):
    description = models.CharField(max_length=500, blank=True)
    document = models.FileField(upload_to='documents/', null=True, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ResearchPapers(models.Model):
    doi = models.CharField(max_length=255,blank=False)
    population =  models.CharField(max_length=255,blank=False)
    intervention = models.CharField(max_length=255, blank=False)
    comparison = models.CharField(max_length=255, blank=False)
    outcome = models.CharField(max_length=255, blank=False)
    context = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default= 'default.jpg', upload_to='profile_pics')
    #enter = models.TextField()


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
