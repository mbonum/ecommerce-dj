# Generated by Django 3.2.4 on 2021-06-23 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20210623_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='background',
            new_name='media',
        ),
    ]
