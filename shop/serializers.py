from rest_framework import serializers

from directory.serializers import ProductCategoryListSerializer, \
    ProductSizeListSerializer
from shop.models import Product, PointsTransaction, QRTutorialSlide, QRScanHistory, QRReward, Cart, CartItem, FAQ
from users.serializers import UserDetailSerializer


# Tarjima asosiy serializeri
class LocaleSerializer(serializers.ModelSerializer):
    name_en = serializers.CharField(allow_blank=False)
    name_uz = serializers.CharField(allow_blank=False)
    name_ru = serializers.CharField(allow_blank=False)


class BaseLocaleSerializer(serializers.ModelSerializer):
    """
    Dinamik ko‘p tilli serializer:
    Modelda mavjud bo‘lgan *_en/_uz/_ru maydonlar avtomatik qo‘shiladi.
    """
    TRANSLATABLE_BASES = [
        # eng ko‘p uchraydiganlar
        'name',
    ]
    LANGS = ['en', 'uz', 'ru']
    REQUIRED_BASES = {'name', }  # muhim maydonlar

    def get_fields(self):
        fields = super().get_fields()
        model = getattr(self.Meta, 'model', None)
        if not model:
            return fields

        # Modeldagi real maydonlar to‘plami
        model_field_names = {f.name for f in model._meta.get_fields()}

        for base in self.TRANSLATABLE_BASES:
            for lang in self.LANGS:
                f_name = f"{base}_{lang}"
                if f_name in model_field_names:
                    fields[f_name] = serializers.CharField(
                        allow_blank=False,
                        required=(base in self.REQUIRED_BASES)
                    )
        return fields


class ProductListSerializer(serializers.ModelSerializer):
    category_detail = ProductCategoryListSerializer(source='category', read_only=True)
    sizes_detail = ProductSizeListSerializer(source='sizes', many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_detail',
            'type',
            'title',
            'subtitle',
            'image',
            'price_points',
            'old_price_points',
            'sizes',
            'sizes_detail',
            'is_one_size',
            'stock',
            'is_limited',
            'is_active',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemListSerializer(serializers.ModelSerializer):
    product_detail = ProductListSerializer(source='product', read_only=True)
    size_detail = ProductSizeListSerializer(source='size', read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'cart',
            'product',
            'product_detail',
            'size',
            'size_detail',
            'quantity',
            'item_points',
        )


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartListSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(source='user', read_only=True)
    items = CartItemListSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'user',
            'user_detail',
            'status',
            'total_points',
            'items',
        )


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class QRRewardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRReward
        fields = ('id', 'code', 'description', 'points', 'is_active', 'used_count', 'max_uses')


class QRRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRReward
        fields = '__all__'


class QRScanHistoryListSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(source='user', read_only=True)
    reward_detail = QRRewardListSerializer(source='reward', read_only=True)

    class Meta:
        model = QRScanHistory
        fields = (
            'id',
            'user',
            'user_detail',
            'reward',
            'reward_detail',
            'points_awarded',
            'scanned_at',
        )


class QRScanHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QRScanHistory
        fields = '__all__'


class QRTutorialSlideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRTutorialSlide
        fields = ('id', 'title', 'description', 'image', 'order')


class QRTutorialSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRTutorialSlide
        fields = '__all__'


class PointsTransactionListSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(source='user', read_only=True)

    class Meta:
        model = PointsTransaction
        fields = ('id', 'user', 'user_detail', 'reason', 'amount', 'comment')


class PointsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsTransaction
        fields = '__all__'


class FAQListSerializer(serializers.ModelSerializer):
    """
    FAQ ro‘yxati uchun serializer (list view, public API va h.k.).
    """
    class Meta:
        model = FAQ
        fields = (
            'id',
            'question',
            'answer',
            'order',
            'is_active',
        )


class FAQSerializer(serializers.ModelSerializer):
    """
    Admin CRUD uchun to‘liq serializer (create/update).
    """
    class Meta:
        model = FAQ
        fields = '__all__'