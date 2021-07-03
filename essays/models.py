from datetime import timezone  # datetime

# from django.template.defaultfilters import slugify
# from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import IntegrityError, models
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from markdown_deux import markdown
from meta.models import ModelMeta
from tinymce.models import HTMLField

# from notes.models import Note
from tags.models import Tag
from team.models import Member


def essay_media_path(self, filename: str):
    return f"essays/{self.slug}/{filename}"


def author_image_path(self, filename: str):
    slug = self.slug
    if filename is not slug:
        filename = slug  # + '_' + self.job_title
    return f"essays/authors-pic/{filename}"


class Author(models.Model):
    name = models.CharField(max_length=90, blank=False, null=True)
    slug = models.SlugField(blank=False, null=True, unique=True)
    bio = HTMLField("Bio", blank=False, null=True)
    img = models.FileField("Pic", upload_to=author_image_path, blank=True, null=True)
    author_url = models.URLField(
        max_length=200, blank=True, null=True, help_text=_("Website of the author")
    )

    class Meta:
        verbose_name_plural = _("Independent authors")

    def __str__(self):
        return self.name

    def img_tag(self):
        if self.img:
            return mark_safe(
                f'<img src="{self.img.url}" style="width:60px; height:60px;"/>'
            )
        else:
            return _("Please add an image")

    img_tag.short_description = _("Image")


class EssayQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(slug__icontains=query)
                # | Q(text__icontains=query)
                | Q(tags__name__icontains=query)
                | Q(tags__slug__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class EssayManager(models.Manager):
    def active(self, *args, **kwargs):
        return (
            super(EssayManager, self)
            .filter(publish=True)
            .filter(updated__lte=timezone.now())
        )

    def get_queryset(self):
        return EssayQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Essay(ModelMeta, models.Model):
    # Add sitemap and SEO metadata
    _metadata = {
        "extra_props": {
            "author": getattr(settings, "ENV_NAME", "Clavem"),
        },
        # 'extra_custom_props': 'get_custom_props'
    }
    index = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=True,
        unique=True,
        default=1,
    )
    img = models.FileField(
        _("Cover image"), upload_to=essay_media_path, blank=True, null=True
    )
    title = models.CharField(max_length=99, blank=False, null=True, db_index=True)
    slug = models.SlugField(blank=False, null=True, unique=True)
    tags = models.ManyToManyField(Tag, blank=False)
    author_team = models.ForeignKey(
        Member, on_delete=models.CASCADE, blank=True, null=True, related_name="C_team"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_("Add if independent author"),
    )
    audio = models.FileField(
        upload_to=essay_media_path, blank=True, null=True, help_text=_("Record reading")
    )
    summary = HTMLField(_("Summary"), blank=True, null=True)
    publish = models.BooleanField(default=False, help_text=_("Edit before publishing"))
    recommend = models.BooleanField(default=False, help_text=_("Must-read"))
    created = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated at"), auto_now=True)
    # language = models.CharField(max_length=2, default='en', choices=LANG_STATUS_CHOICES)
    # essay_rating = RatingField(range=5)# 5 possible rating values, 1-5
    # hit_count_generic = models.IntegerField(HitCountMixin, object_id_field='object_pk',
    # related_query_name='hit_count_generic_relation')
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True), related_names='essay_likes'

    objects = EssayManager()

    class Meta:
        verbose_name_plural = _("Essays")
        ordering = ["index"]

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.img:
            return mark_safe(
                f'<img src="{self.img.url}" style="width:60px; height:60px;">'
            )
        else:
            return _("Please add an image")

    image_tag.short_description = _("Image")

    def get_absolute_url(self):
        # Get the essay through its slug
        return reverse("read:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.name) author is a member of the team or independent
        if self.author_team is not None and self.author_team.name == self.author:
            raise IntegrityError
        super(Essay, self).save(*args, **kwargs)

    # def get_markdown(self):
    #     content = self.body
    #     markdown_text = markdown(content)
    #     return mark_safe(markdown_text)#md->html

    # @property# in views .notes
    # def notes(self):
    #     qs = Note.objects.filter_by_instance(self)
    #     return qs

    # @property
    # def get_content_type(self):
    #     qs = ContentType.objects.get_for_model(self.__class__)
    #     return qs


class SectionQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(slug__icontains=query)
                | Q(text__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class SectionManager(models.Manager):
    # def active(self, *args, **kwargs):
    #     return (
    #         super(EssayManager, self)
    #         .filter(publish=True)
    #         .filter(updated__lte=timezone.now())
    #     )

    def get_queryset(self):
        return SectionQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Section(models.Model):
    essay = models.ForeignKey(
        Essay,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    title = models.CharField(
        help_text=_("Skip if section 1"), max_length=90, blank=True, null=True
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    text = HTMLField(
        blank=False,
        null=True,
        help_text=_(
            'Exordium (Pathos)-> Narratio -> Confirmatio (Logos) -> Refutatio (Ethos) -> Peroration (Pathos)[View->srcode->class="fl"]'
        ),
    )
    img = models.FileField(
        _("Image"), upload_to=essay_media_path, blank=True, null=True
    )

    objects = SectionManager()
