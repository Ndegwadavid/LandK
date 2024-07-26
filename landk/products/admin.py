from django.contrib import admin

# Register your models here.
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'category', 'date_added']
    list_filter = ['category', 'date_added']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['share_id']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:  # Only show share_id for existing objects
            return fields + ['share_id']
        return fields