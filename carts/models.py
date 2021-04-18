from django.conf import settings
from django.core.validators import MinValueValidator  # MaxValueValidator
from django.db import models
from django.db.models.signals import m2m_changed, pre_save  # post_save
from django.utils.translation import gettext_lazy as _
from products.models import Product

USER = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session["cart_id"] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(USER, blank=True, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=False)
    order_qty = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    # for discounts and shipping
    subtotal = models.DecimalField(default=0.00, max_digits=19, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=19, decimal_places=2)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def is_digital(self):
        # Filter digital products to skip ship address form
        qs = self.products.all()
        new_qs = qs.filter(is_digital=False)
        if new_qs.exists():
            return False
        return True


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        products = instance.products.all()
        total = 0
        for _ in products:
            total += _.price
        instance.subtotal = total
        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
