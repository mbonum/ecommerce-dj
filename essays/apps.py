from django.apps import AppConfig

# from django.contrib.admin.apps import AdminConfig

# separate adimn
# class EssaysAdminConfig(AdminConfig):
#     default_site = "essays.admin.EssaysAdminArea"


class EssaysConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "essays"
