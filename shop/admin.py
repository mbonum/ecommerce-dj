from django.contrib import admin
from django.forms import ModelForm

from .models import Category, Product, ProductFile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "index",
        "active",
    )
    list_editable = (
        "index",
        "active",
    )
    prepopulated_fields = {"slug": ("name",)}


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # form = ProductModelForm
    list_display = (
        "name_product",
        "index",
        "price",
        "quantity",
        "active",
        "category",
        "is_digital",
        "recommend",
        "img_tag",
    )
    list_editable = (
        "index",
        "price",
        "quantity",
        "active",
        "category",
        "is_digital",
        "recommend",
    )
    list_filter = ("active", "is_digital", "recommend", "created_at")
    search_fields = (
        "name_product",
        "slug",
    )
    prepopulated_fields = {"slug": ("name_product",)}
    inlines = (ProductFileInline,)
    # list_display_links = ('__str__',)


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
