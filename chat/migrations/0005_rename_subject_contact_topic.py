# Generated by Django 3.2.4 on 2021-06-25 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_contact_postal_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='subject',
            new_name='topic',
        ),
    ]
