# Generated by Django 3.2.6 on 2021-08-28 17:58

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_alter_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(null=True, upload_to=shop.models.shop_media_path, verbose_name='Image/GIF'),
        ),
    ]
