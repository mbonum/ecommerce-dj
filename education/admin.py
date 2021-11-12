from django.contrib import admin
from django.forms import ModelForm
from .models import Book, Section


class SectionInline(admin.TabularInline):
    model = Section
    extra = 2
    prepopulated_fields = {"slug": ("title",)}


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "index", "created", "img_tag")
    inlines = [SectionInline]
    list_editable = ("index",)
    list_filter = ("created",)
    prepopulated_fields = {"slug": ("title",)}

    class Meta:
        model = Book


admin.site.register(Book, BookAdmin)