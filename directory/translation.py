from modeltranslation.translator import register, TranslationOptions

from .models import Region, District, Country, ProductCategory


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
