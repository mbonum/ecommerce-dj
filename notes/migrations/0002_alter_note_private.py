# Generated by Django 3.2 on 2021-04-26 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='private',
            field=models.BooleanField(blank=True, default=False, help_text='Show name/email', null=True),
        ),
    ]
