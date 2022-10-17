from django.db import models
from django.db.models.signals import pre_save  # , post_save

# from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.utils import unique_slug_generator


class Tag(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    # Use signals to set slugs
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)
