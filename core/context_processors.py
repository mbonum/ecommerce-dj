from django.conf import settings


def from_settings(request):
    return {
        "ENV_NAME": getattr(settings, "ENV_NAME", "Clavem") + " DEV",
    }
