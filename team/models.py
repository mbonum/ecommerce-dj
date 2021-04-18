from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


def member_image_path(self, filename):
    slug = self.slug
    if filename is not self.name + "_" + self.job_title:
        filename = self.name + "_" + self.job_title
    return f"team/{slug}/{filename}"  # Save img in static-cdn/media-root/team/{id}


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=True,
        unique=True,
        default=1,
    )
    name = models.CharField(max_length=90, blank=False, null=True)
    slug = models.SlugField(blank=False, unique=True)
    job_title = models.CharField(max_length=90, blank=False)
    bio = HTMLField(_("Bio"), blank=False, null=True)
    img = models.FileField(_("Pic"), upload_to=member_image_path, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, blank=True)
    show = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _("Members")
        ordering = ["index"]

    def __str__(self):
        return self.name

    def img_tag(self):
        if self.img:
            return mark_safe(
                f'<img src="{self.img.url}" style="width:60px; height:60px;"/>'
            )
        else:
            return _("Please add image")

    img_tag.short_description = _("Pic")

    def get_absolute_url(self):
        return reverse(
            "team:detail", kwargs={"slug": self.slug}
        )  # kwargs={'id': self.id})# Get member using its id
