# Generated by Django 3.2.4 on 2021-06-21 19:57

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(choices=[('C', 'Collaboration'), ('J', 'Employment'), ('F', 'Feedback'), ('M', 'Misc')], default='C', max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('subject', models.CharField(max_length=255)),
                ('text', tinymce.models.HTMLField(blank=True, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=19, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
