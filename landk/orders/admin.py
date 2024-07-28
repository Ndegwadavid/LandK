from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'zip_code']

admin.site.register(OrderItem)