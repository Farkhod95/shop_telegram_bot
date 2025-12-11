from modeltranslation.translator import register, TranslationOptions

from shop.models import Product


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle')
