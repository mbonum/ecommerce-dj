# Generated by Django 3.2.4 on 2021-06-11 16:50

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('essays', '0009_rename_image_essay_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essay',
            name='abstract',
        ),
        migrations.AddField(
            model_name='essay',
            name='summary',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Summary'),
        ),
    ]
