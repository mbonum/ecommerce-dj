# Generated by Django 4.1 on 2022-08-17 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("carts", "0001_initial"),
        ("billing", "0001_initial"),
        ("shop", "0001_initial"),
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductPurchase",
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
                ("order_id", models.CharField(max_length=120)),
                ("refunded", models.BooleanField(default=False)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "billing_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billing.billingprofile",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.product"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                ("order_id", models.CharField(max_length=90)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("C", "Created"),
                            ("P", "Paid"),
                            ("S", "Shipped"),
                            ("R", "Refunded"),
                        ],
                        default="C",
                        max_length=9,
                    ),
                ),
                (
                    "shipping_total",
                    models.DecimalField(decimal_places=2, default=9.99, max_digits=19),
                ),
                (
                    "discount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
                ),
                (
                    "subtotal",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "billing_address",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="billing_address",
                        to="addresses.address",
                    ),
                ),
                (
                    "billing_profile",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billing.billingprofile",
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="carts.cart",
                    ),
                ),
                (
                    "shipping_address",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="shipping_address",
                        to="addresses.address",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Orders",
                "ordering": ["-created", "-updated"],
            },
        ),
    ]
