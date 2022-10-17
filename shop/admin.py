from django.contrib import admin
from django.forms import ModelForm
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductFile, Review


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
        "name",
        "index",
        "price",
        "qty_instock",
        "active",
        "category",
        "is_digital",
        # "recommend",
        "img_tag",
    )
    list_editable = (
        "index",
        "price",
        "qty_instock",
        "active",
        "category",
        "is_digital",
        # "recommend",
    )
    list_filter = ("active", "is_digital", "created")  # "recommend",
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (ProductFileInline,)


admin.site.register(Review, MPTTModelAdmin)