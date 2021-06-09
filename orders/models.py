import datetime
from math import fsum

# from django.conf import settings
from django.db import models
from django.db.models import Avg, Count, Sum
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from addresses.models import Address
from core.utils import unique_order_id_generator
from billing.models import BillingProfile
from carts.models import Cart
from products.models import Product


# ORDER_STATUS_CHOICES = [
#     ('created', 'Created'),
#     ('paid', 'Paid'),
#     ('shipped', 'Shipped'),
#     ('refunded', 'Refunded')
# ]
class OrderStatus(models.TextChoices):
    CREATED = "C", _("Created")
    PAID = "P", _("Paid")
    SHIPPED = "S", _("Shipped")
    REFUNDED = "R", _("Refunded")


class OrderManagerQueryset(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated_at", "-created_at")  # The oldest updates last

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        shipped = recent.not_refunded().by_status(status=OrderStatus.SHIPPED)
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status=OrderStatus.PAID)
        paid_data = paid.totals_data()
        data = {
            "recent": recent,
            "recent_data": recent_data,
            "recent_cart_data": recent_cart_data,
            "shipped": shipped,
            "shipped_data": shipped_data,
            "paid": paid,
            "paid_data": paid_data,
        }
        return data

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (number_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date, end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated_at__gte=start_date)
        return self.filter(updated_at__gte=start_date).filter(updated_at__lte=end_date)

    def by_date(self):
        # Sales in the last 15 days
        now = timezone.now() - datetime.timedelta(days=15)
        return self.filter(update_at__day__gte=now.day)  # month__gte=now.month

    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))

    def cart_data(self):
        return self.aggregate(
            Sum("cart__products__price"),
            Avg("cart__products__price"),
            Count("cart__products"),
        )

    def by_status(self, status=OrderStatus.SHIPPED):
        return self.filter(status=status)

    def not_refunded(self):
        return self.exclude(status=OrderStatus.REFUNDED)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status=OrderStatus.CREATED)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQueryset(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status=OrderStatus.CREATED,
        )  # .exclude(status='paid')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile, cart=cart_obj
            )
            created = True
        return obj, created


class Order(models.Model):
    order_id = models.CharField(
        max_length=90, blank=False, null=False
    )  # unique random id: AB383C
    billing_profile = models.ForeignKey(
        BillingProfile, blank=False, null=True, on_delete=models.CASCADE
    )
    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_address",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )
    billing_address = models.ForeignKey(
        Address,
        related_name="billing_address",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=9, choices=OrderStatus.choices, default=OrderStatus.CREATED
    )  # default='created', choices=ORDER_STATUS_CHOICES
    shipping_total = models.DecimalField(default=9.99, max_digits=19, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=19, decimal_places=2)  # %
    subtotal = models.DecimalField(
        default=0.00, max_digits=19, decimal_places=2
    )  # if digital subt=total
    total = models.DecimalField(
        default=0.00, max_digits=19, decimal_places=2
    )  # subtotal + shipping
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name_plural = _("Orders")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={"order_id": self.order_id})

    def get_invoice_url(self):
        return reverse("invoice", kwargs={"_id": self.order_id})

    def get_status(self):
        # Only for non-digital products
        if self.status == OrderStatus.REFUNDED:
            return _("Refunded order")
        elif self.status == OrderStatus.SHIPPED:
            return _("Shipped")
        return _("Shipping Soon")

    def update_total(self):
        # Add quantity
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = fsum([cart_total, shipping_total])
        formatted_total = format(new_total, ".2f")
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        shipping_address_required = not self.cart.is_digital
        # if digital no shipment
        shipping_done = False
        if shipping_address_required and self.shipping_address:
            shipping_done = True
        elif shipping_address_required and not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_done and billing_address and total > 0:
            return True
        return False

    def update_purchases(self):
        for _p in self.cart.products.all():
            obj, created = ProductPurchase.objects.get_or_create(
                order_id=self.order_id, product=_p, billing_profile=self.billing_profile
            )
        return ProductPurchase.objects.filter(order_id=self.order_id).count()

    def mark_paid(self):
        if self.status != OrderStatus.PAID:
            if self.check_done():
                self.status = OrderStatus.PAID
                self.save()
                self.update_purchases()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(
        billing_profile=instance.billing_profile
    )
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    # The post signal is activated once the user clicks on save
    if not created:
        # cart_total = instance.total
        qs = Order.objects.filter(cart__id=instance.id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)


class ProductPurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)

    def digital(self):
        return self.filter(product__is_digital=True)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)


class ProductPurchaseManager(models.Manager):
    def get_queryset(self):
        return ProductPurchaseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def digital(self):
        return self.get_queryset().active().digital()

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def products_by_id(self, request):
        qs = self.by_request(request).digital()
        ids_ = [x.product.id for x in qs]
        return ids_

    def products_by_request(self, request):
        ids_ = self.products_by_id(request)
        products_qs = Product.objects.filter(id__in=ids_).distinct()
        return products_qs


class ProductPurchase(models.Model):
    # billing_profile.productpurchase_set.all()
    order_id = models.CharField(max_length=120)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # product.productpurchase_set.count()
    refunded = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductPurchaseManager()

    def __str__(self):
        return self.product.title
