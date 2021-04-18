# Generated by Django 3.1.7 on 2021-03-30 11:41

import django.core.validators
from django.db import migrations, models
import team.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveSmallIntegerField(default=1, null=True, unique=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('name', models.CharField(max_length=90, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('job_title', models.CharField(max_length=90)),
                ('bio', tinymce.models.HTMLField(null=True, verbose_name='Bio')),
                ('img', models.FileField(blank=True, null=True, upload_to=team.models.member_image_path, verbose_name='Pic')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('show', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Members',
                'ordering': ['index'],
            },
        ),
    ]
