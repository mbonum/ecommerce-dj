# Generated by Django 4.1 on 2022-08-17 10:01

from django.conf import settings
import django.core.files.storage
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import pathlib
import shop.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="Name"
                    ),
                ),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("active", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ["index"],
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                ("slug", models.SlugField(null=True, unique=True)),
                (
                    "img",
                    models.ImageField(
                        null=True,
                        upload_to=shop.models.shop_media_path,
                        verbose_name="Image/GIF",
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True, null=True, upload_to=shop.models.shop_media_path
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=9.99,
                        max_digits=9,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Price (€)",
                    ),
                ),
                (
                    "text",
                    tinymce.models.HTMLField(
                        help_text="Benefits per cost",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "is_digital",
                    models.BooleanField(
                        default=True, help_text="No shipment", verbose_name="Digital"
                    ),
                ),
                (
                    "order_qty",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "qty_instock",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Quantity in stock",
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=False,
                        help_text="Hide if unavailable",
                        verbose_name="Show",
                    ),
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
                    "pdf",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=shop.models.shop_media_path,
                        verbose_name="PDF Brochure/Manual",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="shop.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Products",
                "ordering": ["index"],
            },
        ),
        migrations.CreateModel(
            name="Review",
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
                ("body", tinymce.models.HTMLField(null=True, verbose_name="Review")),
                (
                    "stars",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=True, help_text="Hide useless ones", verbose_name="Show"
                    ),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="shop.product",
                    ),
                ),
                (
                    "like",
                    models.ManyToManyField(
                        blank=True, related_name="like", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="shop.review",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductFile",
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
                    "file",
                    models.FileField(
                        storage=django.core.files.storage.FileSystemStorage(
                            location=pathlib.PurePosixPath(
                                "/home/mgb/cw/media/protected"
                            )
                        ),
                        upload_to=shop.models.upload_product_file_loc,
                    ),
                ),
                ("free", models.BooleanField(default=False)),
                ("user_required", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.product"
                    ),
                ),
            ],
        ),
    ]
