# Generated by Django 3.2.6 on 2021-08-24 14:59

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_product_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.shop_media_path),
        ),
    ]
