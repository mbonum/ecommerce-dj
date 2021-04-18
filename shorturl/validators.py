from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


def validate_url(value):
    url_validator = URLValidator()
    reg_value = value
    if "https" in reg_value:
        new_value = reg_value
    else:
        new_value = "https://" + value
    try:
        url_validator(new_value)
    except:
        raise ValidationError(_("Please submit a valid URL"), code="invalid")
    return value


def validate_dotcom_url(value):
    if not "co" in value:
        raise ValidationError(_("Please submit a .co URL"), code='invalid')
    return value
