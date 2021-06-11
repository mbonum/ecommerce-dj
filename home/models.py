from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class Page(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    background = models.FileField(upload_to="homepage/", blank=True, null=True)
    # title_btn = models.CharField(max_length=255, blank=True, null=True) max_length=100
    # title_btn_url = models.CharField(max_length=255, blank=True, null=True)
    description = HTMLField(blank=True, null=True)
    quote = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Homepage")


class MessageType(models.TextChoices):
    COLLABORATION = "C", _("Collaboration")
    EMPLOYMENT = "J", _("Employment")
    FEEDBACK = "F", _("Feedback")
    MISC = "M", _("Misc")


class Contact(models.Model):
    message_type = models.CharField(
        max_length=255, choices=MessageType.choices, default=MessageType.COLLABORATION
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    text = HTMLField(blank=True, null=True)
    postal_code = models.CharField(max_length=19, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    # confirm = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "email", "subject", "text", "postal_code"]

    # objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = _("Contacts")


class Donate(models.Model):
    title = models.CharField(max_length=250)
    btc_desc = HTMLField(_("BTC Description"), blank=True, null=True)
    btc = models.CharField(max_length=250, blank=True, null=True)
    eth_desc = HTMLField(_("ETH Description"), blank=True, null=True)
    eth = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Donate page")


class Cookie(models.Model):
    title = models.CharField(max_length=99)
    text = HTMLField(blank=False, null=True, help_text=_("Clear, concise, no legalese"))
    pdf = models.FileField(
        "PDF", upload_to="cookie/", max_length=100, blank=True, null=True
    )
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Cookie policy")


class Privacy(models.Model):
    title = models.CharField(max_length=99)
    text = HTMLField(blank=False, null=True, help_text=_("Clear, concise, no legalese"))
    pdf = models.FileField(
        "PDF", upload_to="privacy/", max_length=255, blank=True, null=True
    )
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Privacy policy")

    # def get_absolute_url(self):
    #     return reverse("home:detail", kwargs={"order_id": self.order_id})


# class Return(models.Model):
#     title = models.CharField(max_length=99)
#     text = HTMLField(blank=False, null=True, help_text=_("Clear, concise, no legalese"))
#     pdf = models.FileField(
#         "PDF", upload_to="return/", max_length=255, blank=True, null=True
#     )
#     updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = _("Return policy")


class Terms(models.Model):
    title = models.CharField(max_length=250)
    text = HTMLField(
        _("Terms"), blank=False, null=True, help_text=_("Clear, concise, no legalese")
    )
    pdf = models.FileField(
        "PDF", upload_to="terms/", max_length=255, blank=True, null=True
    )
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Terms of use")


# transparency Imprint
class Trademark(models.Model):
    title = models.CharField(max_length=99)
    text = HTMLField(blank=False, null=True, help_text=_("Clear, concise, no legalese"))
    pdf = models.FileField(
        "PDF", upload_to="Trademark/", max_length=255, blank=True, null=True
    )
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Trademark")


# Terms of Use on a website are terms which apply to every visitor. Terms and Conditions apply to particular users of the website, usually when the user is required to pay for a product and/or service.


# class Email(models.Model):
## Add Email Policy if required
#     title = models.CharField(max_length=250)
#     sec1 = HTMLField('Body 1', blank=True, null=True)# models.TextField(blank=True, null=True)
#     section2 = models.CharField(max_length=250, blank=True, null=True)
#     sec2 = HTMLField('Body 2', blank=True, null=True)
#     section3 = models.CharField(max_length=250, blank=True, null=True)
#     sec3 = HTMLField('Body 3', blank=True, null=True)
#     pdf = models.FileField(upload_to='email/', max_length=100, blank=True, null=True)
#     updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = 'Email policy'
