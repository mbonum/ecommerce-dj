from core.utils import create_shortcode
from django.conf import settings
from django_hosts.resolvers import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_url  # validate_dotcom_url,

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 7)
# URL = getattr(settings, "BASE_URL", "https://www.clavem.co")


class ClUrlManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(ClUrlManager, self).all(*args, **kwargs).filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = ClUrl.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by("-id")[:items]
        new = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            new += 1
        return f"New codes created {new}"


class ClUrl(models.Model):
    # id = models.AutoField(primary_key=True)
    url = models.CharField(
        max_length=240, validators=[validate_url]  # , validate_dotcom_url
    )
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    # null=False
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClUrlManager()

    class Meta:
        verbose_name = _("Clvm short URL")
        verbose_name_plural = _("Clvm short URLs")
        ordering = ["-updated"]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        if not "https" in self.url:
            self.url = "https://" + self.url
        super(ClUrl, self).save(*args, **kwargs)

    def get_short_url(self):
        url_path = reverse(
            "clvmcode", kwargs={"shortcode": self.shortcode}, host="www", scheme="http"
        )  # , port="8000"
        return url_path
