from django_filters.rest_framework import FilterSet

from shop.models import Product, Cart, CartItem, QRReward, QRScanHistory, QRTutorialSlide, PointsTransaction, FAQ


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'type': ['exact'],
            'title': ['icontains'],
            'is_limited': ['exact'],
            'is_active': ['exact'],
        }


class CartFilter(FilterSet):
    class Meta:
        model = Cart
        fields = {
            'user': ['exact'],
            'status': ['exact'],
        }


class CartItemFilter(FilterSet):
    class Meta:
        model = CartItem
        fields = {
            'cart': ['exact'],
            'product': ['exact'],
            'size': ['exact'],
        }


class QRRewardFilter(FilterSet):
    class Meta:
        model = QRReward
        fields = {
            'code': ['exact', 'icontains'],
            'is_active': ['exact'],
        }


class QRScanHistoryFilter(FilterSet):
    class Meta:
        model = QRScanHistory
        fields = {
            'user': ['exact'],
            'reward': ['exact'],
        }


class QRTutorialSlideFilter(FilterSet):
    class Meta:
        model = QRTutorialSlide
        fields = {
            'title': ['icontains'],
        }


class PointsTransactionFilter(FilterSet):
    class Meta:
        model = PointsTransaction
        fields = {
            'user': ['exact'],
            'reason': ['exact'],
        }


class FAQFilter(FilterSet):
    class Meta:
        model = FAQ
        fields = {
            'is_active': ['exact'],
        }