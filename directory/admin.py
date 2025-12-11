from django.contrib import admin
from directory.models import (
    District, Region, Country, ProductCategory, ProductSize
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    fields = ('name', 'name_en', 'name_uz', 'name_ru', 'name_lt', 'code')
    search_fields = ('name', 'name_en', 'name_uz', 'name_ru', 'name_lt', 'code')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    fields = ('name', 'name_en', 'name_uz', 'name_ru', 'name_lt', 'code')
    search_fields = ('name', 'name_en', 'name_uz', 'name_ru', 'name_lt', 'code')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'region')
    fields = ('name', 'name_en', 'name_uz', 'name_ru', 'name_lt', 'code', 'region', 'geo_json')
    search_fields = ('name', 'name_en', 'name_uz', 'name_ru', 'name_lt', 'code')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    fields = ('name', 'slug', 'order')
    search_fields = ('name', 'slug')


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('label', 'order')
    fields = ('label', 'order')
    search_fields = ('label',)