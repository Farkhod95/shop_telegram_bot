from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from directory.models import Region, District, Country, ProductCategory, ProductSize
from restapp.models import BaseModel
User = settings.AUTH_USER_MODEL

class Product(BaseModel):
    """
    Market va Розыгрышdagi barcha obyektlar (futbolka, huddi, krossovka, iPhone va h.k.).
    - type:
        MARKET  – oddiy market, tugma “В корзину”, Cart orqali sotib olinadi.
        RAFFLE – розыгрыш, tugma “Играть”, foydalanuvchi ball sarflab o‘yin o‘ynaydi.
    - price_points / old_price_points – hozirgi va eski ball narxi (chegirma ko‘rsatish uchun).
    - sizes / is_one_size – o‘lchamlar bilan ishlash (“Размер” / “Один размер” selectlari).
    - stock, is_limited, is_active – ombor va aktivlik nazorati.
    """

    class ProductType(models.TextChoices):
        MARKET = 'market', _('Market')       # 2-rasm: “В корзину”
        RAFFLE = 'raffle', _('Розыгрыш')     # 3-rasm: “Играть”

    category = models.ForeignKey( ProductCategory, related_name='products', on_delete=models.CASCADE, verbose_name=_('Kategoriya'),)
    type = models.CharField(_('Turi'),max_length=20,choices=ProductType.choices,default=ProductType.MARKET,)
    title = models.CharField(_('Nomi'), max_length=255)
    subtitle = models.CharField(_('Qisqa tavsif'), max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='burn/products/%Y/%m/%d')
    price_points = models.PositiveIntegerField(_('Ball narxi'))
    old_price_points = models.PositiveIntegerField(_('Eski ball narxi'), null=True, blank=True, help_text=_('Chegirma ko‘rsatish uchun'),)
    sizes = models.ManyToManyField( ProductSize, related_name='products', blank=True, verbose_name=_('Mavjud o‘lchamlar'),)
    is_one_size = models.BooleanField(_('Bitta o‘lcham'), default=False, help_text=_('“Один размер” tugmasi uchun'),)
    stock = models.PositiveIntegerField(_('Ombordagi soni'), default=0)
    is_limited = models.BooleanField(_('Limited'), default=False)
    is_active = models.BooleanField(_('Aktiv'), default=True)

    class Meta:
        verbose_name = _('Mahsulot')
        verbose_name_plural = _('Mahsulotlar')

    def __str__(self):
        return self.title


class Cart(BaseModel):
    """
    Foydalanuvchining savatchasi (Корзина).
    - Har bir BurnUser uchun bir nechta cart bo‘lishi mumkin (ochiq, yakunlangan va h.k.).
    - total_points – savatchadagi mahsulotlar umumiy ball narxi (balansni tekshirish uchun).
    - Telegram botda katalogdan “В корзину” bosilganda CartItem lar shu yerga yig‘iladi.
    """

    class Status(models.TextChoices):
        OPEN = 'open', _('Ochiq')
        CHECKED_OUT = 'checked_out', _('Yakunlangan')
        CANCELED = 'canceled', _('Bekor qilingan')

    user = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE, verbose_name=_('Foydalanuvchi'))
    status = models.CharField(_('Status'), max_length=20, choices=Status.choices, default=Status.OPEN)
    total_points = models.PositiveIntegerField(_('Jami ball'), default=0, help_text=_('Hisob-kitobni tezlashtirish uchun denormalizatsiya'))

    class Meta:
        verbose_name = _('Savatcha')
        verbose_name_plural = _('Savatchalar')

    def __str__(self): return f'Cart #{self.id} - {self.user}'


class CartItem(BaseModel):
    """
    Savatchadagi bitta mahsulot yozuvi.
    - product: qaysi mahsulot.
    - size: tanlangan o‘lcham (agar bo‘lsa).
    - quantity: nechta dona.
    - item_points: bitta CartItem uchun jami ball (price_points * quantity),
      keyin Cart.total_points ni hisoblashda ishlatiladi.
    """

    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name=_('Savatcha'))
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE, verbose_name=_('Mahsulot'))
    size = models.ForeignKey(ProductSize, related_name='cart_items', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('O‘lcham'))
    quantity = models.PositiveIntegerField(_('Soni'), default=1)
    item_points = models.PositiveIntegerField(_('Jami ball'), default=0, help_text=_('product.price_points * quantity'))

    class Meta:
        verbose_name = _('Savatcha elementi')
        verbose_name_plural = _('Savatcha elementlari')


class QRReward(BaseModel):
    """
    QR kod / havola orqali beriladigan mukofot konfiguratsiyasi.
    - code: QR ichidagi token yoki link parametri (unikal).
    - points: bir marta skan qilinganda beriladigan ball.
    - max_uses / used_count: umumiy necha marta ishlatilishi mumkinligini cheklash.
    - is_active: QR hozir aktivmi yoki bloklangan.
    4-rasmdagi “Сканируй QR-коды, получай баллы” logikasini backendda ta’minlaydi.
    """

    code = models.CharField(_('QR kodi yoki token'), max_length=255, unique=True, help_text=_('Skan qilinganda botga keladigan kod'))
    description = models.CharField(_('Izoh'), max_length=255, null=True, blank=True)
    points = models.PositiveIntegerField(_('Beriladigan ballar'), default=0)
    max_uses = models.PositiveIntegerField(_('Maksimal ishlatish soni'), null=True, blank=True)
    used_count = models.PositiveIntegerField(_('Necha marta ishlatilgan'), default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('QR mukofoti')
        verbose_name_plural = _('QR mukofotlari')

    def __str__(self): return self.code


class QRScanHistory(BaseModel):
    """
    Foydalanuvchilarning QR kodlarni skan qilish tarixi.
    - Har bir skan uchun user, qaysi QRReward, necha ball berildi va vaqtini yozib boradi.
    - Statistikalar, antifraud va support uchun kerak bo‘ladi (“sen bu QRni allaqachon ishlatgansan” va h.k.).
    """

    user = models.ForeignKey(User, related_name='qr_scans', on_delete=models.CASCADE, verbose_name=_('Foydalanuvchi'))
    reward = models.ForeignKey(QRReward, related_name='scans', on_delete=models.CASCADE, verbose_name=_('Mukofot'))
    points_awarded = models.PositiveIntegerField(_('Berilgan ballar'), default=0)
    scanned_at = models.DateTimeField(_('Skan qilingan vaqt'), auto_now_add=True)

    class Meta:
        verbose_name = _('QR skan tarixi')
        verbose_name_plural = _('QR skan tarixi')


class QRTutorialSlide(BaseModel):
    """
    “Как сканировать QR-код?” bo‘limidagi slaydlar (1/4, 2/4, 3/4, 4/4).
    - Har bir slayd uchun sarlavha, matn va rasm saqlanadi.
    - order bo‘yicha tartiblanadi.
    Frontda foydalanuvchiga QR skan qilish bo‘yicha vizual instruktsiya ko‘rsatish uchun.
    """

    title = models.CharField(_('Sarlavha'), max_length=255)
    description = models.TextField(_('Tavsif'), blank=True)
    image = models.ImageField(upload_to='burn/qr_tutorial/%Y/%m/%d')
    order = models.PositiveIntegerField(_('Tartib raqami'), default=0)

    class Meta:
        verbose_name = _('QR bo‘yicha slayd')
        verbose_name_plural = _('QR bo‘yicha slaydlar')
        ordering = ['order']

    def __str__(self): return self.title


class PointsTransaction(BaseModel):
    """
    Ball balansidagi o‘zgarishlar tarixi (ledger).
    - Har qanday ball qo‘shish / ayirish shu yerda yoziladi:
      QR skan, market xarid, rozigrishda ishtirok, referal bonusi, profilni to‘ldirish va h.k.
    - amount: ijobiy bo‘lsa ball qo‘shiladi, manfiy bo‘lsa balansdan ayriladi.
    - reason: ball nimaga berilganini aniq ko‘rsatish (hisob-kitob va audit uchun).
    UIda “b 0” ikonkasini ko‘rsatish, balansni qayta hisoblash, istoriyani chiqarish uchun asosiy model.
    """

    class Reason(models.TextChoices):
        QR_SCAN = 'qr_scan', _('QR skan')
        MARKET_PURCHASE = 'market_purchase', _('Marketdan xarid')
        RAFFLE_PLAY = 'raffle_play', _('Розыгрышда ishtirok')
        REFERRAL_BONUS = 'referral_bonus', _('Referal bonus')
        PROFILE_BONUS = 'profile_bonus', _('Profilni to‘ldirish bonusi')
        OTHER = 'other', _('Boshqa')

    user = models.ForeignKey(User, related_name='points_transactions', on_delete=models.CASCADE, verbose_name=_('Foydalanuvchi'))
    reason = models.CharField(_('Sabab'), max_length=32, choices=Reason.choices, default=Reason.OTHER)
    amount = models.IntegerField(_('Miqdori'), help_text=_('Musbat – qo‘shiladi, manfiy – ayriladi'))
    comment = models.CharField(_('Izoh'), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Ball tranzaksiyasi')
        verbose_name_plural = _('Ball tranzaksiyalari')

    def __str__(self): return f'{self.user} | {self.amount} ({self.reason})'


class FAQ(BaseModel):
    """
    FAQ (Часто задаваемые вопросы) bo‘limi uchun model.
    - question: savol matni
    - answer: javob matni (HTML bo‘lishi ham mumkin)
    - order: tartiblash uchun
    - is_active: faqat aktivlari front va botga beriladi
    """
    question = models.CharField(_('Savol'), max_length=255)
    answer = models.TextField(_('Javob'))
    order = models.PositiveIntegerField(_('Tartib raqami'), default=0)
    is_active = models.BooleanField(_('Aktiv'), default=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQlar')
        ordering = ['order', 'id']

    def __str__(self):
        return self.question