"""
Education models (add other contents such as films)
from django.db.models.signals import pre_save, post_save
"""
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from tags.models import Tag


def book_media_path(self, filename):
    return f"edu/{self.slug}/{filename}"


class BookQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(slug__icontains=query)
                # | Q(text_icontains=query)
                | Q(tags__name__icontains=query)
                | Q(tags__slug__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class BookManager(models.Manager):
    def active(self, *args, **kwargs):
        return (
            super(BookManager, self)
            .filter(publish=True)
            .filter(updated__lte=timezone.now())
        )

    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, _id):
        qs = self.get_queryset().filter(id=_id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Book(models.Model):
    # id = models.AutoField(primary_key=True)
    index = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=True,
        unique=True,
        default=1,
    )
    title = models.CharField(max_length=90, db_index=True)
    slug = models.SlugField(blank=False, unique=True)
    tags = models.ManyToManyField(Tag, blank=False)
    text = HTMLField(_("Key points"), blank=False, null=True)
    audio = models.FileField(_("Record reading"), upload_to=book_media_path, blank=True, null=True)
    img = models.ImageField(_("Cover"), upload_to=book_media_path, blank=False, null=True)
    created = models.DateTimeField(_("Created at"), auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(_("Publish"), default=True)

    objects = BookManager()

    class Meta:
        verbose_name_plural = _("Books")
        ordering = ["index"]

    def __str__(self):
        return self.title

    def img_tag(self):
        if self.img:
            return mark_safe(
                f'<img src="{self.img.url}" style="width:60px; height:60px;"/>'
            )
        else:
            return _("Please add an image")

    img_tag.short_description = _("Cover")

    def get_absolute_url(self):
        return reverse('learn:booknotes', kwargs={'slug': self.slug})

    @property
    def name(self):
        return self.title
