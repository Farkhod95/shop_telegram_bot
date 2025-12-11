from django.contrib import admin
from .models import ( Product,
    Cart, CartItem, QRReward, QRScanHistory,
    QRTutorialSlide, PointsTransaction, FAQ
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_en', 'title_uz', 'title_ru', 'category', 'type', 'price_points', 'stock', 'is_limited', 'is_active')
    fields = ('category', 'type', 'title', 'title_en', 'title_uz', 'title_ru', 'subtitle', 'subtitle_en', 'subtitle_uz', 'subtitle_ru', 'image', 'price_points', 'old_price_points',
              'sizes', 'is_one_size', 'stock', 'is_limited', 'is_active')
    search_fields = ('title', 'subtitle')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_points')
    fields = ('user', 'status', 'total_points')
    search_fields = ('user__full_name', 'user__username', 'user__telegram_id')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'size', 'quantity', 'item_points')
    fields = ('cart', 'product', 'size', 'quantity', 'item_points')
    search_fields = ('cart__id', 'product__title')


@admin.register(QRReward)
class QRRewardAdmin(admin.ModelAdmin):
    list_display = ('code', 'points', 'max_uses', 'used_count', 'is_active')
    fields = ('code', 'description', 'points', 'max_uses', 'used_count', 'is_active')
    search_fields = ('code',)


@admin.register(QRScanHistory)
class QRScanHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'points_awarded', 'scanned_at')
    fields = ('user', 'reward', 'points_awarded', 'scanned_at')
    search_fields = ('user__full_name', 'reward__code')


@admin.register(QRTutorialSlide)
class QRTutorialSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    fields = ('title', 'description', 'image', 'order')
    search_fields = ('title',)


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'amount')
    fields = ('user', 'reason', 'amount', 'comment')
    search_fields = ('user__full_name', 'reason')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    fields = ('question', 'answer', 'order', 'is_active')
    search_fields = ('question',)