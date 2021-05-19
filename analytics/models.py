"""
Add page viewed analytics and share with the user
"""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.db import models
from django.db.models.signals import post_save  # , pre_save

from accounts.signals import USER_LOGGED_IN
from shorturl.models import ClUrl
from .signals import OBJECT_VIEWED_SIGNAL
from .utils import get_client_ip

USER = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, "FORCE_SESSION_TO_ONE", False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, "FORCE_INACTIVE_USER_ENDSESSION", False)


class ClickEventManager(models.Manager):
    def create_event(self, clInstance):
        if isinstance(clInstance, ClUrl):
            obj, created = self.get_or_create(cl_url=clInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    cl_url = models.OneToOneField(ClUrl, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return self.cl_url.url + " -> Clicks: " + f"{self.count}"

    class Meta:
        ordering = ["-updated"]
        verbose_name = _("Count URL clicks")
        verbose_name_plural = _("Count URL clicks")


class ObjectViewedQueryset(models.query.QuerySet):
    def by_model(self, model_class, model_queryset=False):
        c_type = ContentType.objects.get_for_model(model_class)
        qs = self.filter(content_type=c_type)
        if model_queryset:
            viewed_ids = [x.object_id for x in qs]
            # equivalent of viewed_ids = [] for x in views: viewed_ids.append(x.object_id)
            return model_class.objects.filter(pk__in=viewed_ids)
        return qs


class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQueryset(self.model, using=self._db)

    def by_model(self, model_class, model_queryset=False):
        return self.get_queryset().by_model(model_class, model_queryset=model_queryset)


class ObjectViewed(models.Model):
    user = models.ForeignKey(USER, blank=True, null=True, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()  # User id, Product id, Order, Cart, Address etc.
    content_object = GenericForeignKey("content_type", "object_id")  # Product instance
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return f"{self.content_object} viewed: {self.created_at}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Object Viewed")
        verbose_name_plural = _("Objects Viewed")


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    user = None
    if request.user.is_authenticated:
        user = request.user
    if not ObjectViewed.objects.filter(user=user, content_type=c_type, object_id=instance.id).exists():
        new_view_obj = ObjectViewed.objects.create(
            user=user,
            content_type=c_type,
            object_id=instance.id,
            ip_address=get_client_ip(request),
        )


OBJECT_VIEWED_SIGNAL.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(USER, blank=True, null=True, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    session_key = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            raise Http404("?")
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()


if settings.FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):

    if not created:
        if instance.is_active is False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()


if settings.FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=USER)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(user=user, ip_address=ip_address, session_key=session_key)


USER_LOGGED_IN.connect(user_logged_in_receiver)
