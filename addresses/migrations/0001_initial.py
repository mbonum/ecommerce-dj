# Generated by Django 4.1 on 2022-08-17 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                    "address_type",
                    models.CharField(
                        choices=[("B", "Billing"), ("S", "Shipping")],
                        default="B",
                        max_length=9,
                    ),
                ),
                ("street", models.CharField(blank=True, max_length=240, null=True)),
                ("city", models.CharField(max_length=240)),
                ("state", models.CharField(blank=True, max_length=240, null=True)),
                ("country", models.CharField(default="Earth", max_length=240)),
                ("postal_code", models.CharField(default="41280", max_length=10)),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "billing_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billing.billingprofile",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Addresses",
            },
        ),
    ]
