# Generated by Django 2.2.3 on 2020-05-21 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DatabaseSearch_Datatable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=255)),
                ('Year', models.IntegerField(blank=True)),
                ('Url', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'ordering': ['Title'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500)),
                ('document', models.FileField(null=True, upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResearchPapers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doi', models.CharField(max_length=255)),
                ('population', models.CharField(max_length=255)),
                ('intervention', models.CharField(max_length=255)),
                ('comparison', models.CharField(max_length=255)),
                ('outcome', models.CharField(max_length=255)),
                ('context', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Snowballing_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Papers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]