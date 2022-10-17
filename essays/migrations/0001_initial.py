# Generated by Django 4.1 on 2022-08-17 10:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import essays.models
import meta.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tags", "0001_initial"),
        ("team", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=90, null=True)),
                ("slug", models.SlugField(null=True, unique=True)),
                ("bio", tinymce.models.HTMLField(null=True, verbose_name="Bio")),
                (
                    "img",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=essays.models.author_image_path,
                        verbose_name="Pic",
                    ),
                ),
                (
                    "author_url",
                    models.URLField(
                        blank=True, help_text="Website of the author", null=True
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Independent authors",
            },
        ),
        migrations.CreateModel(
            name="Essay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "index",
                    models.PositiveSmallIntegerField(
                        default=1,
                        null=True,
                        unique=True,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "img",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=essays.models.essay_media_path,
                        verbose_name="Cover image",
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=99, null=True)),
                ("slug", models.SlugField(null=True, unique=True)),
                (
                    "audio",
                    models.FileField(
                        blank=True,
                        help_text="Record reading",
                        null=True,
                        upload_to=essays.models.essay_media_path,
                    ),
                ),
                (
                    "summary",
                    tinymce.models.HTMLField(
                        blank=True, null=True, verbose_name="Summary"
                    ),
                ),
                (
                    "publish",
                    models.BooleanField(
                        default=False, help_text="Edit before publishing"
                    ),
                ),
                (
                    "recommend",
                    models.BooleanField(default=False, help_text="Must-read"),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        help_text="Add if independent author",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="essays.author",
                    ),
                ),
                (
                    "author_team",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="C_team",
                        to="team.member",
                    ),
                ),
                ("tags", models.ManyToManyField(to="tags.tag")),
            ],
            options={
                "verbose_name_plural": "Essays",
                "ordering": ["index"],
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="Skip if section 1",
                        max_length=90,
                        null=True,
                    ),
                ),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                (
                    "text",
                    tinymce.models.HTMLField(
                        help_text='Exordium (Pathos)-> Narratio -> Confirmatio (Logos) -> Refutatio (Ethos) -> Peroration (Pathos)[View->srcode->class="fl"]',
                        null=True,
                    ),
                ),
                (
                    "img",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=essays.models.essay_media_path,
                        verbose_name="Image",
                    ),
                ),
                (
                    "essay",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="essays.essay",
                    ),
                ),
            ],
        ),
    ]
