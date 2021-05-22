import os
import random

from core.utils import get_filename, unique_slug_generator  # random_string_generator
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator  # MaxValueValidator
from django.db import models
from django.db.models import Q  # search
from django.db.models.signals import pre_save  # post_save
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from tags.models import Tag

# from djmoney.models.fields import MoneyField

from accounts.models import CUser


# def get_filename_ext(filepath):
#     # Get the extension of a file
#     basename = os.path.basename(filepath)
#     name, ext = os.path.splitext(basename)
#     return name, ext


# def upload_image_path(self, filename):
#     # Add random image name
#     new_filename = random.randint(1, 999999999)
#     name, ext = get_filename_ext(filename)
#     final_filename = f"{new_filename}{ext}"
#     return f"products/{new_filename}/{final_filename}"


def product_img_path(self, filename):
    # Save file in static-cdn/media-root/products/...
    slug = self.slug
    return f"products/{slug}/{filename}"


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def is_digital(self):
        return self.filter(is_digital=True, active=True)

    # def featured(self):
    #     return self.filter(available=True, active=True)

    def search(self, query):
        lookups = (
            Q(slug__icontains=query)
            | Q(description__icontains=query)
            | Q(price__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(tags__slug__icontains=query)
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def digital(self):
        # Skip shipping address form in checkout
        self.quantity = 1
        self.in_stock = True
        return self.get_queryset().is_digital()

    # def featured(self):
    #     # Product.objects.featured()
    #     # if self.quantity >= 1:
    #     #     return self.get_queryset().featured()
    #     # else:
    #     #     return self.filter(featured=False, active=False)# sold out
    #     return self.get_queryset().featured()  # available

    def get_by_id(self, _id):
        qs = self.get_queryset().filter(id=_id)
        if qs.count() == 1:
            return qs.first()
        return None

    def check_inventory(self):
        # Check whether there are inventory inconsistencies
        if self.quantity > 0 and self.active == False:
            raise ValueError(f"Check product {self.name} inventory")

    def search(self, query):
        return self.get_queryset().active().search(query)


class ProductType(models.TextChoices):
    EBOOK = "E", _("Ebook")  # is_digital=True
    AUDIO = "A", _("Audio")
    PHYSICAL = "P", _("Physical")  # is_digital=False -> delivery


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=255, db_index=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    index = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=True,
        unique=True,
        default=1,
    )
    name_product = models.CharField(
        _("Name"), max_length=255, blank=True, null=True, db_index=True
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    tags = models.ManyToManyField(Tag, blank=False)
    product_type = models.CharField(
        max_length=8, choices=ProductType.choices, default=ProductType.EBOOK
    )
    category = models.ForeignKey(
        Category,
        related_name="product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # created_by = models.ForeignKey(
    #     CUser,
    #     related_name="product_creator",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    description = HTMLField(_("Benefits"), blank=True, null=True)
    price = models.DecimalField(
        _("Price"),
        decimal_places=2,
        max_digits=9,
        default=99.99,
        validators=[MinValueValidator(0)],
        help_text="EUR",
    )  # MoneyField(max_digits=9, decimal_places=2, default_currency='USD')# IntegerField(default=9999)#cents
    # currency = models.ForeignKey(User.currency, related_name='currency', null=True, blank=True, on_delete=models.CASCADE)
    img = models.ImageField(
        _("Image"), upload_to=product_img_path, blank=True, null=True
    )
    is_digital = models.BooleanField(
        default=False, help_text=_("Digital (in stock, no shipment)")
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    # meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    # meta_description = models.CharField(max_length=255, help_text='Content for description meta tag')
    in_stock = models.BooleanField(_("In Stock"), default=False)
    active = models.BooleanField(
        _("Show"), default=True, help_text=_("Hide if unavailable")
    )
    recommend = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    pdf = models.FileField(
        upload_to="products/", blank=True, null=True
    )  # manual if diy

    objects = ProductManager()

    class Meta:
        verbose_name_plural = _("Products")
        ordering = ["index"]
        # index_together = [('name_product', 'slug'),]

    def __str__(self):
        return self.name_product

    def img_tag(self):
        if self.img:
            return mark_safe(
                f'<img src="{self.img.url}" style="width:60px; height:60px;"/>'
            )
        else:
            return _("Please add an image")

    img_tag.short_description = _("Image")

    def get_absolute_url(self):
        # namespace[in mgb/urls]:name[in app-name/urls]
        return reverse("products:detail", kwargs={"slug": self.slug})

    # def display_price(self):
    #     return "{0:.2f}".format(self.price / 100)

    def rangeqty(self):
        q = []
        if not self.is_digital and self.quantity > 1:
            q = list(range(1, self.quantity + 1))
        return q

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs

    @property
    def name(self):
        return self.name_product


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    """Use signals to set slugs"""
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = f"products/{slug}/"
    return location + filename  # /static_cdn/protected_root/products/slug/file


class ProductFile(models.Model):
    # id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=upload_product_file_loc,
        storage=FileSystemStorage(location=getattr(settings, "PROTECTED_ROOT")),
    )
    free = models.BooleanField(default=False)  # purchase required by default
    user_required = models.BooleanField(default=False)  # user doesn't matter

    def __str__(self):
        return str(self.file.name)

    # def get_default_url(self):
    #         return self.product.get_absolute_url()

    def get_download_url(self):
        return reverse(
            "products:download", kwargs={"slug": self.product.slug, "pk": self.pk}
        )  # self.file.url

    @property
    def name(self):
        return get_filename(self.file.name)
