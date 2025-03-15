from django.contrib import admin
from .models import Product, Coupons, Category, Order, OrderItems


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_sub")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category__name", "price", "available")
    list_filter = ("available", "category")
    search_fields = ("title", "category__name")
    list_editable = ("price", "available")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "paid", "created", "updated", "coupon")
    list_filter = ("paid", "created", "updated")
    search_fields = ("user__username",)
    readonly_fields = ("created", "updated")


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")
    list_filter = ("order", "product")
    search_fields = ("order__user__username", "product__title")


@admin.register(Coupons)
class CouponsAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "is_active", "valid_from", "valid_until")
    list_filter = ("is_active", "valid_from", "valid_until")
    search_fields = ("code",)
    list_editable = ("is_active",)