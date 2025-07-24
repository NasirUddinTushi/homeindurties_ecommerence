from django.contrib import admin
from .models import (
    Cart, CartItem, Coupon, Order, OrderItem,
    ShippingAddress, Payment, OrderStatusUpdate, PaymentFailure
)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__title')

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'full_name', 'city', 'country', 'postal_code')
    search_fields = ('full_name', 'order__id')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'method', 'transaction_id', 'is_paid', 'paid_at')
    search_fields = ('transaction_id',)
    list_filter = ('method', 'is_paid')

@admin.register(OrderStatusUpdate)
class OrderStatusUpdateAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'updated_at')
    list_filter = ('status',)

@admin.register(PaymentFailure)
class PaymentFailureAdmin(admin.ModelAdmin):
    list_display = ('order', 'reason', 'timestamp')
    search_fields = ('order__id',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active', 'expires_at')
    search_fields = ('code',)
    list_filter = ('active',)
