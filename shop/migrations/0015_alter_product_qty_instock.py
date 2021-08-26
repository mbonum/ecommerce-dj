# Generated by Django 3.2.6 on 2021-08-24 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_rename_quantity_product_qty_instock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='qty_instock',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantity in stock'),
        ),
    ]
