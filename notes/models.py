# from django.core.validators import MinValueValidator
# from django.db import IntegrityError, models
# from django.db.models import Q# search
# from django.template.defaultfilters import slugify
# from django.urls import reverse
from django.conf import settings

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.db import models

# from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from mptt.models import MPTTModel, TreeForeignKey
from essays.models import Essay

USER = settings.AUTH_USER_MODEL


class NoteManager(models.Manager):
    def all(self):
        qs = super(NoteManager, self).filter(parent=None)
        return qs

    # def filter_by_instance(self, instance):
    #     c_type = ContentType.objects.get_for_model(instance.__class__)
    #     _id = instance.id
    #     qs = super(NoteManager, self).filter(content_type=c_type, obj_id=_id).filter(parent=None)#.order_by('-created_at')
    #     return qs


class Note(MPTTModel):
    user = models.ForeignKey(USER, blank=False, null=True, on_delete=models.CASCADE)
    essay = models.ForeignKey(
        Essay, blank=False, null=True, on_delete=models.CASCADE, related_name="notes"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    body = HTMLField(_("Note"), blank=False, null=True)
    private = models.BooleanField(
        blank=True, null=True, default=True, help_text=_("Show name/email")
    )
    # reply = models.BooleanField('Activate reply + email notification', blank=True, null=True, default=True)
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False
    )
    active = models.BooleanField(
        _("Show"), default=True, help_text=_("Hide insulting ones")
    )
    like = models.ManyToManyField(USER, blank=True, related_name="likes")

    objects = NoteManager()

    # class Meta:
    #     ordering = ['-created']# higher likes # put the most interesting at the top

    class MPTTMeta:
        verbose_name_plural = _("Notes")
        order_insertion_by = ["created_at"]

    def __str__(self):
        if self.user.first_name:
            n = self.user.first_name
        else:
            n = self.user.email
        return f"Note #{self.id} about {self.essay} by {n}"

    def tot_likes(self):
        return self.like.count()

    # def child(self):#reply
    #     return Note.objects.filter(parent=self)

    # @property
    # def is_parent(self):
    #     if self.parent is not None:
    #         return False
    #     return True
