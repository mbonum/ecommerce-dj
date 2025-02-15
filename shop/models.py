# import os
# import random
from io import BytesIO

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage

# from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator  # MaxValueValidator
from django.db import models
from django.db.models import Q  # search
from django.db.models.signals import pre_save  # post_save
from django.urls import reverse
from django.utils.html import format_html

# from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from tinymce.models import HTMLField

from core.utils import get_filename, unique_slug_generator  # random_string_generator

# from tags.models import Tag

# from djmoney.models.fields import MoneyField

# from accounts.models import CUser

USER = settings.AUTH_USER_MODEL

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


def shop_media_path(self, filename):
    # Save file in static-cdn/media-root/products/...
    _s = self.slug  # add category
    return f"shop/{_s}/{filename}"


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
            | Q(text__icontains=query)
            | Q(price__icontains=query)
            # | Q(tags__name__icontains=query)
            # | Q(tags__slug__icontains=query)
        )
        return self.filter(lookups).distinct()


# class ProductType(models.TextChoices):
#     EBOOK = "E", _("Ebook")  # is_digital=True
#     AUDIO = "A", _("Audio")
#     PHYSICAL = "P", _("Physical")  # is_digital=False -> delivery


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def digital(self):
        # Skip shipping address form in checkout
        if (
            self.category.name == "Audiobooks" or self.category.name == "Ebooks"
        ):  # product_type != ProductType.PHYSICAL:
            self.qty_instock = 1
            # self.in_stock = True
            return self.get_queryset().is_digital()

    # def featured(self):
    #     # Product.objects.featured()
    #     # if self.qty_instock >= 1:
    #     #     return self.get_queryset().featured()
    #     # else:
    #     #     return self.filter(featured=False, active=False)# sold out
    #     return self.get_queryset().featured()  # available

    def get_by_id(self, _id):
        _qs = self.get_queryset().filter(id=_id)
        if _qs.count() == 1:
            return _qs.first()
        return None

    def check_inventory(self):
        # Check whether there are inventory inconsistencies
        if self.qty_instock > 0 and self.active is False:
            _n = self.name
            raise ValueError(f"Check product {_n} inventory")

    def search(self, query):
        return self.get_queryset().active().search(query)


# To add when the variety of products increases
class Category(models.Model):
    index = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=True,
        unique=True,
        default=1,
    )
    name = models.CharField(_("Name"), max_length=255, db_index=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _("Categories")
        ordering = ["index"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category", kwargs={"slug": self.slug})


class Product(models.Model):
    index = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=True,
        unique=True,
        default=1,
    )
    name = models.CharField(
        _("Name"), max_length=255, blank=False, null=True, db_index=True
    )
    slug = models.SlugField(blank=False, null=True, unique=True)
    img = models.ImageField(
        _("Image/GIF"), upload_to=shop_media_path, blank=False, null=True
    )
    thumbnail = models.ImageField(upload_to=shop_media_path, blank=True, null=True)
    # stock_price
    price = models.DecimalField(  # retail_price
        _("Price (€)"),
        blank=False,
        null=True,
        decimal_places=2,
        max_digits=9,
        default=9.99,
        validators=[MinValueValidator(0)],
        # help_text="EUR",
    )  # MoneyField(max_digits=9, decimal_places=2, default_currency='USD')
    # IntegerField(default=9999)#cents
    # currency = models.ForeignKey(CUser.currency, related_name='currency',
    # null=True, blank=True, on_delete=models.SET_NULL)
    # tags = models.ManyToManyField(Tag, blank=False)
    # product_type = models.CharField(
    #     max_length=8, choices=ProductType.choices, default=ProductType.EBOOK
    # )
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        blank=False,
        null=True,
    )
    # sku # stock keeping unit warehouse
    # brand
    # created_by = models.ForeignKey(
    #     CUser,
    #     related_name="product_creator",
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    text = HTMLField(
        _("Description"), blank=False, null=True, help_text=_("Benefits per cost")
    )
    is_digital = models.BooleanField(
        _("Digital"), default=True, help_text=_("No shipment")
    )
    order_qty = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    qty_instock = models.PositiveIntegerField(
        _("Quantity in stock"), default=1, validators=[MinValueValidator(1)]
    )
    total_item = models.DecimalField(
        default=0.00, max_digits=19, decimal_places=2
    )  # order_qty*retail_price
    # meta_keywords = models.CharField(max_length=255,
    # help_text='Comma-delimited set of SEO keywords for meta tag')
    # meta_description = models.CharField(max_length=255,
    # help_text='Content for description meta tag')
    active = models.BooleanField(  # in_stock
        _("Show"), default=False, help_text=_("Hide if unavailable")
    )
    # recommend = models.BooleanField(default=False)
    created = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated at"), auto_now=True)
    pdf = models.FileField(
        _("PDF Brochure/Manual"), upload_to=shop_media_path, blank=True, null=True
    )  # 10-page preview manual if diy

    objects = ProductManager()

    class Meta:
        verbose_name_plural = _("Products")
        ordering = ["index"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.img)
        super().save(*args, **kwargs)

    def img_tag(self):
        if self.thumbnail:
            return format_html(
                f'<img src="{self.thumbnail.url}" style="width:60px; height:60px;">'
            )
        else:
            return _("Image missing")

    img_tag.short_description = _("Image")

    def get_absolute_url(self):
        return reverse(
            "shop:detail", kwargs={"cslug": self.category.slug, "slug": self.slug}
        )

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.img:
                self.thumbnail = self.make_thumbnail(self.img)
                self.save()
                return self.thumbnail.url
            else:
                return ""

    def make_thumbnail(self, image, size=(256, 300)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, "PNG", optimize=True, quality=99)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    @property
    def total_item(self):
        return f"{round(self.order_qty * self.price, 2)}"
        # return "{0:.2f}".format(float(self.order_qty * self.price))

    # If price is in cents
    # def display_price(self):
    #     return "{0:.2f}".format(self.price / 100)

    # def rangeqty(self):
    #     q = []
    #     if not self.is_digital and self.qty_instock > 0:
    #         q = list(range(1, self.qty_instock + 1))
    #     return q

    # Update inventory after an order has been submitted -> signal

    def get_downloads(self):
        _qs = self.productfile_set.all()
        return _qs


def product_pre_save_receiver(instance, **kwargs):  # sender, *args
    # Use signals to set slugs
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = f"shop/{slug}/"  # shop_media_path
    return location + filename  # /static_cdn/protected_root/products/slug/file


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=upload_product_file_loc,
        storage=FileSystemStorage(location=getattr(settings, "PROTECTED_ROOT")),
    )
    free = models.BooleanField(default=False)  # purchase required by default
    user_required = models.BooleanField(default=False)  # user doesn't matter

    def __str__(self):
        return str(self.file.name)

    def get_default_url(self):
        return self.product.get_absolute_url()

    def get_download_url(self):
        return reverse(
            "shop:download", kwargs={"slug": self.product.slug, "pk": self.pk}
        )  # self.file.url

    @property
    def name(self):
        return get_filename(self.file.name)


# class Item(models.Model):
#     category = models.ForeignKey(
#         Category, related_name="items", on_delete=models.CASCADE
#     )
#     parent = models.ForeignKey(
#         "self", related_name="variants", on_delete=models.CASCADE, blank=True, null=True
#     )
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(
#         _("Price (€)"),
#         blank=False,
#         null=True,
#         decimal_places=2,
#         max_digits=9,
#         default=9.99,
#         validators=[MinValueValidator(0)],
#     )
#     is_featured = models.BooleanField(default=False)
#     num_available = models.IntegerField(default=1)
#     num_visits = models.IntegerField(default=0)
#     last_visit = models.DateTimeField(blank=True, null=True)

#     image = models.ImageField(upload_to="uploads/", blank=True, null=True)
#     thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-date_added"]

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         self.thumbnail = self.make_thumbnail(self.image)
#         super().save(*args, **kwargs)

#     def get_absolute_url(self):
#         return f"/{self.category.slug}/{self.slug}/"  # /%s/%s/" % (self.category.slug, self.slug)

#     def get_thumbnail(self):
#         if self.thumbnail:
#             return self.thumbnail.url
#         else:
#             if self.image:
#                 self.thumbnail = self.make_thumbnail(self.image)
#                 self.save()

#                 return self.thumbnail.url
#             else:
#                 return ""

#     def make_thumbnail(self, image, size=(300, 200)):
#         img = Image.open(image)
#         img.convert("RGB")
#         img.thumbnail(size)

#         thumb_io = BytesIO()
#         img.save(thumb_io, "PNG", quality=85)  # "JPEG"

#         thumbnail = File(thumb_io, name=image.name)

#         return thumbnail

#     def get_rating(self):
#         total = sum(int(review["stars"]) for review in self.reviews.values())

#         if self.reviews.count() > 0:
#             return total / self.reviews.count()
#         else:
#             return 0


# class ProductImage(models.Model):
#     product = models.ForeignKey(Item, related_name="images", on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="uploads/", blank=True, null=True)
#     thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)

#     def save(self, *args, **kwargs):
#         self.thumbnail = self.make_thumbnail(self.image)

#         super().save(*args, **kwargs)

#     def make_thumbnail(self, image, size=(300, 200)):
#         img = Image.open(image)
#         img.convert("RGB")
#         img.thumbnail(size)

#         thumb_io = BytesIO()
#         img.save(thumb_io, "PNG", quality=85)  # "JPEG"

#         thumbnail = File(thumb_io, name=image.name)

#         return thumbnail


class Review(MPTTModel):
    user = models.ForeignKey(
        USER, blank=False, null=True, on_delete=models.CASCADE
    )  # related_name="reviews"
    item = models.ForeignKey(
        Product,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    body = HTMLField(_("Review"), blank=False, null=True)
    stars = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    active = models.BooleanField(
        _("Show"), default=True, help_text=_("Hide useless ones")
    )
    like = models.ManyToManyField(USER, blank=True, related_name="like")

    class MPTTMeta:
        verbose_name_plural = _("Reviews")
        order_insertion_by = ["created"]

    def __str__(self):
        if self.user.first_name:
            _n = self.user.first_name
        else:
            _n = self.user.email
        return f"Review #{self.id} about {self.item} by {_n}"

    def tot_likes(self):
        return self.like.count()


# compare md5 to remove duplicate files
# class MediaFileSystemStorage(FileSystemStorage):
#     def get_available_name(self, name, max_length=None):
#         if max_length and len(name) > max_length:
#             raise (Exception("name's length is greater than max_length"))
#         return name

#     def _save(self, name, content):
#         if self.exists(name):
#             # if the file exists, do not call the superclasses _save method
#             return name
#         # if the file is new, DO call it
#         return super(MediaFileSystemStorage, self)._save(name, content)


# def media_file_name(instance, filename):
#     h = instance.md5sum
#     basename, ext = os.path.splitext(filename)
#     return os.path.join("media", h[0:1], h[1:2], h + ext.lower())


# class Media(models.Model):
#     # use the custom storage class fo the FileField
#     orig_file = models.FileField(
#         upload_to=media_file_name, storage=MediaFileSystemStorage()
#     )
#     md5sum = models.CharField(max_length=36)

#     def save(self, *args, **kwargs):
#         if not self.pk:  # file is new
#             md5 = hashlib.md5()
#             for chunk in self.orig_file.chunks():
#                 md5.update(chunk)
#             self.md5sum = md5.hexdigest()
#         super(Media, self).save(*args, **kwargs)
