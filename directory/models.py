from django.db import models
from django.utils.translation import gettext_lazy as _

from restapp.models import BaseModel


class Country(BaseModel):
    code = models.CharField(_('Country code'), max_length=50, null=True, blank=True, help_text=_("Mamlakat kodi"))
    name = models.CharField(max_length=255, null=True, blank=True, help_text=_("Mamlakat nomi"))

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name


class Region(BaseModel):
    code = models.CharField(_('Region code'), max_length=50, null=True, blank=True, help_text=_("Viloyat kodi"))
    name = models.CharField(max_length=255, null=True, blank=True, help_text=_("Viloyat nomi"))
    geo_json = models.TextField(_('GeoJson'), blank=True, help_text=_("Deo json"))

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    def __str__(self):
        return f"{self.code}"


class District(BaseModel):
    code = models.CharField(_('District code'), max_length=50, null=True, blank=True, help_text=_("Tuman kodi"))
    name = models.CharField(_('District name'), max_length=255, null=True, blank=True, help_text=_("Tuman nomi"))
    region = models.ForeignKey(Region, related_name='districts', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Viloyat jadvali bilan bog'lanish"))
    geo_json = models.TextField(_('GeoJson'), blank=True, help_text=_("Geo json"))

    class Meta:
        verbose_name = _('district')
        verbose_name_plural = _('districts')

    def __str__(self):
        return self.name


class ProductCategory(BaseModel):
    """
    Market va Розыгрыш bo‘limlaridagi mahsulot kategoriyalari.
    Masalan: Hit, Burn, Overdose, Banger.
    Frontda blok sarlavhasi sifatida chiqadi, tartib order bo‘yicha boshqariladi.
    """
    name = models.CharField(_('Kategoriya nomi'), max_length=255)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(_('Tartib raqami'), default=0)

    class Meta:
        verbose_name = _('Mahsulot kategoriyasi')
        verbose_name_plural = _('Mahsulot kategoriyalari')
        ordering = ['order']

    def __str__(self):
        return self.name


class ProductSize(BaseModel):
    """
    Mahsulot o‘lchamlari: S, M, L, XL va hokazo.
    Har bir Product bir nechta size’ga ega bo‘lishi mumkin.
    """
    label = models.CharField(_('O‘lcham'), max_length=50)
    order = models.PositiveIntegerField(_('Tartib raqami'), default=0)

    class Meta:
        verbose_name = _('O‘lcham')
        verbose_name_plural = _('O‘lchamlar')
        ordering = ['order']

    def __str__(self):
        return self.label

