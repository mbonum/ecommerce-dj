"""
Custom user
Require email instead of username
Consider removing password -> Passwordless
Register -> send email to verify and activate account
Login -> send email every time -> enforce 2fa
"""
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import (
    send_mail,
)  # https://docs.djangoproject.com/en/3.1/topics/email/
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from core.utils import unique_key_generator

# send_mail(subject, message, from_email, recipient_list, html_message) random_string_generator,

DEFAULT_ACTIVATION_DAYS = getattr(settings, "DEFAULT_ACTIVATION_DAYS", 7)
C = getattr(settings, "ENV_NAME", "Clavem")

# CURRENCIES = [
#     ('€', 'EUR'),
#     ('$', 'USD'),
#     # ('£', 'GBP'), Add crypto
#     # ('$', 'CAD'),
#     # ('$', 'AUS'),
# ]
class CurrencyType(models.TextChoices):
    EUR = "EUR", _("EURO")
    USD = "USD", _("US Dollar")


class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email and password.
    """

    def create_user(
        self, email, password=None, fn=None, **kwargs
    ):  # ln=None, staff=False, active=True, admin=False
        if not email:
            raise ValueError(_("Please add your email address"))
        if not password:
            raise ValueError(_("Please set your password"))
        if not fn:
            raise ValueError(_("Please add your name"))
        e = self.normalize_email(email)  # self.model(email=self.normalize_email(email))
        user = self.model(email=e, first_name=fn, **kwargs)
        user.set_password(password)
        # user.first_name = fn# Use first name to send personalize email
        # user.last_name = ln
        # user.is_staff = staff
        # user.is_active = active
        # user.is_superuser = admin
        # user.date_joined.timezone.now()
        user.save(using=self._db)
        return user

    def create_staffuser(
        self, email, password=None, first_name=None, **kwargs
    ):  # last_name=None,
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        if kwargs.get("is_active") is False:
            raise ValueError(_("Forgot active=True"))
        if kwargs.get("is_staff") is False:
            raise ValueError(_("Forgot staff=True"))
        if kwargs.get("is_superuser") is False:
            raise ValueError(_("Staff is not admin"))
        return self.create_user(email, password, first_name, **kwargs)

    def create_superuser(self, email, password=None, first_name=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_active") is False:
            raise ValueError("Forgot to set is_active=True")
        if kwargs.get("is_staff") is False:
            raise ValueError("Forgot to set is_active=True")
        if kwargs.get("is_superuser") is False:# remove
            raise ValueError("Forgot to set is_superuser=True")
        return self.create_user(email, password, first_name, **kwargs)


def user_image_path(self, filename):
    u = self.first_name + "-" + self.last_name
    return f"users/{u}/{filename}"


class CUser(AbstractBaseUser, PermissionsMixin):
    # id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=150, unique=True)  # db_index=True
    # username = CharField(max_length=90, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    bio = HTMLField(_("Bio"), blank=False, null=True)
    # img = models.FileField('Profile', upload_to=user_image_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # click on the link
    # is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        _("Date joined"), auto_now_add=True
    )  # default=timezone.now
    currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.EUR
    )
    # confirm = models.BooleanField(default=False)blank=True, null=True,
    # confirmed_date = models.DateTimeField(auto_now_add=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        abstract = False

    def __str__(self):
        return self.email

    # def get_username(self):
    #     """Consider using email as username"""
    #     if self.full_name:email
    #        return self.full_name
    #     if self.username:
    #        return self.username
    #     return self.first_name

    def get_full_name(self):
        return str(self.first_name + self.last_name)

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def staff(self):
        if self.is_superuser:
            return True
        return self.is_staff

    @property
    def superuser(self):
        return self.is_superuser

    @property
    def active(self):
        return self.is_active


class EmailActivationQuerySet(models.query.QuerySet):
    """EmailActivation.objects.all().confirmable()"""

    def confirmable(self):
        """Does the object have a timestamp"""
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        # activated = False
        # forced_expired = False
        return self.filter(activated=False, forced_expired=False).filter(
            timestamp__gt=start_range,  # greater
            timestamp__lte=end_range,  # less or equal
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        """EmailActivation.objects.confirmable()"""
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        """Check if email is present in the database"""
        return (
            self.get_queryset()
            .filter(Q(email=email) | Q(user__email=email))
            .filter(activated=False)
        )


class EmailActivation(models.Model):
    """Expire after 7 days"""
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, null=True, blank=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    # def activate(self):
    #     if self.can_activate():
    #         # pre activation user signal
    #         user = self.user
    #         user.is_active = True
    #         user.save()
    #         # post activation signal for user
    #         self.activated = True
    #         self.save()
    #         return True
    #     return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, "BASE_URL", "https://www.clavem.co/")
                key_path = reverse("account:email-activate", kwargs={"key": self.key})
                path = f"{base_url}/{key_path}"  #'{base}{path}'.format(base=base_url, path=key_path)
                context = {"path": path, "email": self.email}
                subject = (
                    "Activate your " + C + " account"
                )  # (expire in 1 week) Verify Email
                txt_ = get_template("registration/emails/verify.txt").render(context)
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                html_ = get_template("registration/emails/verify.html").render(context)
                sent_mail = send_mail(  ### [Errno 101] Network is unreachable
                    subject,
                    txt_,  # message
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,  # change to True in production
                )
                return sent_mail
            return False


def pre_save_email_activation(sender, instance, *args, **kwargs):

    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):

    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()  ###[Errno 101] Network is unreachable


post_save.connect(post_save_user_create_receiver, sender=CUser)
