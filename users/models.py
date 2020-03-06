from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ResearchPapers(models.Model):
    doi = models.CharField(max_length=255,blank=False)
    population =  models.CharField(max_length=255,blank=False)
    intervention = models.CharField(max_length=255, blank=False)
    context = models.CharField(max_length=255, blank=False)
    outcome = models.CharField(max_length=255, blank=False)
    comparison = models.CharField(max_length=255, blank=False)



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
