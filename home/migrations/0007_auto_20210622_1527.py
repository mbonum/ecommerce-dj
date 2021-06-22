# Generated by Django 3.2.4 on 2021-06-22 15:27

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210618_2114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cookie',
            old_name='updated_at',
            new_name='updated',
        ),
        migrations.RenameField(
            model_name='privacy',
            old_name='updated_at',
            new_name='updated',
        ),
        migrations.RenameField(
            model_name='terms',
            old_name='updated_at',
            new_name='updated',
        ),
        migrations.AlterField(
            model_name='section',
            name='text',
            field=tinymce.models.HTMLField(help_text='Legal Design', null=True),
        ),
    ]
