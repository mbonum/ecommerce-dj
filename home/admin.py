from django.contrib import admin

from .models import Cookie, Donate, Page, Privacy, Terms

# admin.site.register(Contact)Contact,
admin.site.register(Cookie)
admin.site.register(Donate)
admin.site.register(Page)
admin.site.register(Privacy)
admin.site.register(Terms)
