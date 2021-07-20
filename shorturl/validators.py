from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


def validate_url(url):
    url_validator = URLValidator()
    if "http" in url or "https" in url:
        new_url = url.replace("http://www.", "https://")
        print("@@@@@@ ", new_url)
    # reg_value = value
    # if "https" in reg_value or "http" in reg_value:
    #     new_url = reg_value
    # else:
    #     new_url = "https://" + value
    try:
        url = url_validator(new_url)  # url_validator(new_value)
        print("^^^^^ ", new_url)
    except:
        raise ValidationError(_("Please submit a valid URL"), code="invalid")
    return new_url


def validate_dotcom_url(value):
    if not "co" or not "com" in value:
        raise ValidationError(_("Please submit a .co or .com URL"), code="invalid")
    return value


# def validate_url(value):
#     url_valid = URLValidator()
#     url_1_invalid = False
#     url_2_invalid = False
#     try:
#         url_valid(value)
#     except:
#         url_1_invalid = True
#     url_2_invalid = 'http://' + value
#     try:
#         url_valid(url_2_invalid)
#     except:
#         url_2_invalid = True
#     if url_1_invalid == False and url_2_invalid == False:
#         raise ValidationError(_("Please submit a valid URL"))
#     return value