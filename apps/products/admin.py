from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Review, Tag

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductVariantInline]
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'description')

admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductVariantInline]
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'description')
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")
    search_fields = ("product__title",)

admin.site.register(Review)
admin.site.register(Tag)