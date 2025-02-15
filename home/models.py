from django.conf import settings

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

CLVM = getattr(settings, "ENV_NAME", "Clavem")


def policy_media_path(self, filename: str):
    # Set path for policies
    slug = self.slug
    if filename is not slug:
        filename = slug
    if CLVM in filename:
        return f"policies/{filename}.pdf"
    else:
        return f"policies/{CLVM}-{filename}.pdf"


class Page(models.Model):
    # Homepage contents
    title = models.CharField(max_length=255, blank=True, null=True)
    media = models.FileField(upload_to="home/", blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    quote = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Homepage")


class MessageType(models.TextChoices):
    # Create email routing system
    COLLABORATION = "C", _("Collaboration")
    EMPLOYMENT = "J", _("Employment")
    FEEDBACK = "F", _("Feedback")
    MISC = "M", _("Misc")


class Contact(models.Model):
    # Contact form -> Async Chat
    message_type = models.CharField(
        max_length=255, choices=MessageType.choices, default=MessageType.COLLABORATION
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    text = HTMLField(blank=True, null=True)
    postal_code = models.CharField(max_length=19, blank=True, null=True)
    created = models.DateTimeField(_("Created at"), auto_now_add=True)
    # valid = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "email", "subject", "text", "postal_code"]

    # objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = _("Contacts")


class Donate(models.Model):
    # Show crypto wallet public addresses
    title = models.CharField(max_length=250)
    btc_desc = HTMLField(_("BTC Text"), blank=True, null=True)
    btc = models.CharField(max_length=42, blank=True, null=True)
    eth_desc = HTMLField(_("ETH Text"), blank=True, null=True)
    eth = models.CharField(max_length=42, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Donate page")


class Cookie(models.Model):
    title = models.CharField(max_length=99)
    slug = models.SlugField(blank=True, null=True, unique=True)
    pdf = models.FileField(
        "PDF", upload_to=policy_media_path, max_length=100, blank=True, null=True
    )
    updated = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Cookie policy")


# A policy is made by multiple sections
class CSection(models.Model):
    policy = models.ForeignKey(Cookie, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(
        help_text=_("Skip if section 1"), max_length=99, blank=True, null=True
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    text = HTMLField(
        blank=False, null=True, help_text=_("Legal Design. Clear. Concise. No legalese")
    )
    img = models.FileField(
        _("Image"), upload_to=policy_media_path, blank=True, null=True
    )


class Privacy(models.Model):
    title = models.CharField(max_length=99)
    slug = models.SlugField(blank=True, null=True, unique=True)
    pdf = models.FileField(
        "PDF", upload_to=policy_media_path, max_length=255, blank=True, null=True
    )
    updated = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Privacy policy")

    # def get_absolute_url(self):
    #     return reverse("home:detail", kwargs={"order_id": self.order_id})


class PSection(models.Model):
    policy = models.ForeignKey(Privacy, on_delete=models.CASCADE, blank=True, null=True)
    # object_id = models.PositiveIntegerField()
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # content_object = GenericForeignKey("content_type", "object_id")
    title = models.CharField(
        help_text=_("Skip if section 1"), max_length=99, blank=True, null=True
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    text = HTMLField(
        blank=False, null=True, help_text=_("Legal Design. Clear. Concise. No legalese")
    )
    img = models.FileField(
        _("Image"), upload_to=policy_media_path, blank=True, null=True
    )


# Terms of Use on a website are terms which apply to every visitor.
# Terms and Conditions apply to particular users of the website,
# usually when the user is required to pay for a product and/or service.
class Terms(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True, unique=True)
    pdf = models.FileField(
        "PDF", upload_to=policy_media_path, max_length=255, blank=True, null=True
    )
    updated = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Terms of use")


class TSection(models.Model):
    policy = models.ForeignKey(Terms, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(
        help_text=_("Skip if section 1"), max_length=99, blank=True, null=True
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    text = HTMLField(
        blank=False, null=True, help_text=_("Legal Design. Clear. Concise. No legalese")
    )
    img = models.FileField(
        _("Image"), upload_to=policy_media_path, blank=True, null=True
    )


class Trademark(models.Model):
    title = models.CharField(max_length=99)
    text = HTMLField(
        blank=False, null=True, help_text=_("Legal Design. Clear. Concise. No legalese")
    )
    pdf = models.FileField(
        "PDF", upload_to=policy_media_path, max_length=255, blank=True, null=True
    )
    updated = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Trademark")


# Imprint

# class Email(models.Model):
# Add Email Policy if required
#     title = models.CharField(max_length=250)
#     sec1 = HTMLField('Body 1', blank=True, null=True)# models.TextField(blank=True, null=True)
#     section2 = models.CharField(max_length=250, blank=True, null=True)
#     sec2 = HTMLField('Body 2', blank=True, null=True)
#     section3 = models.CharField(max_length=250, blank=True, null=True)
#     sec3 = HTMLField('Body 3', blank=True, null=True)
#     pdf = models.FileField(upload_to=policy_media_path, max_length=100, blank=True, null=True)
#     updated = models.DateTimeField(_('Updated at'), auto_now=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = _('Email policy')


# class Return(models.Model):
#     title = models.CharField(max_length=99)
#     text = HTMLField(blank=False, null=True, help_text=_("Clear, concise, no legalese"))
#     pdf = models.FileField(
#         "PDF", upload_to=policy_media_path, max_length=255, blank=True, null=True
#     )
#     updated = models.DateTimeField(_("Updated at"), auto_now=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = _("Return policy")
