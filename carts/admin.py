from django.contrib import admin

# Register your models here.
from carts.models import Cart, CartItem


class CartItemAdmin(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [CartItemAdmin]
    list_display = ['user', 'price', 'total_price', 'status']


admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem)
