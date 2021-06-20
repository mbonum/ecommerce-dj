# Generated by Django 3.2.4 on 2021-06-18 21:14

from django.db import migrations, models
import django.db.models.deletion
import home.models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('home', '0005_delete_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='description',
            new_name='text',
        ),
        migrations.AddField(
            model_name='privacy',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='privacy',
            name='pdf',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=home.models.policy_media_path, verbose_name='PDF'),
        ),
        migrations.AlterField(
            model_name='trademark',
            name='pdf',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='trademark/', verbose_name='PDF'),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, help_text='Skip if section 1', max_length=90, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('text', tinymce.models.HTMLField(help_text='Exordium (Pathos)-> Narratio -> Confirmatio (Logos) -> Refutatio (Ethos) -> Peroration (Pathos)[View->srcode->class="fl"]', null=True)),
                ('img', models.FileField(blank=True, null=True, upload_to=home.models.policy_media_path, verbose_name='Image')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
