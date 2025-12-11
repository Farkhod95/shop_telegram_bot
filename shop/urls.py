from django.urls import re_path, path

from shop.views.cart import CartView, CartDetailView, CartFieldInfoView
from shop.views.cart_item import CartItemView, CartItemDetailView, CartItemFieldInfoView
from shop.views.faq import FAQView, FAQDetailView, FAQFieldInfoView
from shop.views.points_transaction import PointsTransactionView, PointsTransactionDetailView, \
    PointsTransactionFieldInfoView
from shop.views.product import ProductView, ProductDetailView, ProductFieldInfoView
from shop.views.qr_reward import QRRewardView, QRRewardDetailView, QRRewardFieldInfoView
from shop.views.qr_scan_history import QRScanHistoryView, QRScanHistoryDetailView, QRScanHistoryFieldInfoView
from shop.views.qr_tutorial_slide import QRTutorialSlideView, QRTutorialSlideDetailView, QRTutorialSlideFieldInfoView

urlpatterns = [
    # Product
    re_path(r'^products$', ProductView.as_view(), name='products_view'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='products_detail_view'),
    path('products/fields/', ProductFieldInfoView.as_view(), name='products_fields_info'),

    # Cart
    re_path(r'^carts$', CartView.as_view(), name='carts_view'),
    path('carts/<int:pk>', CartDetailView.as_view(), name='carts_detail_view'),
    path('carts/fields/', CartFieldInfoView.as_view(), name='carts_fields_info'),

    # CartItem
    re_path(r'^cart-items$', CartItemView.as_view(), name='cart_items_view'),
    path('cart-items/<int:pk>', CartItemDetailView.as_view(), name='cart_items_detail_view'),
    path('cart-items/fields/', CartItemFieldInfoView.as_view(), name='cart_items_fields_info'),

    # QRReward
    re_path(r'^qr-rewards$', QRRewardView.as_view(), name='qr_rewards_view'),
    path('qr-rewards/<int:pk>', QRRewardDetailView.as_view(), name='qr_rewards_detail_view'),
    path('qr-rewards/fields/', QRRewardFieldInfoView.as_view(), name='qr_rewards_fields_info'),

    # QRScanHistory
    re_path(r'^qr-scan-history$', QRScanHistoryView.as_view(), name='qr_scan_history_view'),
    path('qr-scan-history/<int:pk>', QRScanHistoryDetailView.as_view(), name='qr_scan_history_detail_view'),
    path('qr-scan-history/fields/', QRScanHistoryFieldInfoView.as_view(), name='qr_scan_history_fields_info'),

    # QRTutorialSlide
    re_path(r'^qr-tutorial-slides$', QRTutorialSlideView.as_view(), name='qr_tutorial_slides_view'),
    path('qr-tutorial-slides/<int:pk>', QRTutorialSlideDetailView.as_view(), name='qr_tutorial_slides_detail_view'),
    path('qr-tutorial-slides/fields/', QRTutorialSlideFieldInfoView.as_view(), name='qr_tutorial_slides_fields_info'),

    # PointsTransaction
    re_path(r'^points-transactions$', PointsTransactionView.as_view(), name='points_transactions_view'),
    path('points-transactions/<int:pk>', PointsTransactionDetailView.as_view(), name='points_transactions_detail_view'),
    path('points-transactions/fields/', PointsTransactionFieldInfoView.as_view(),
         name='points_transactions_fields_info'),

    # FAQ
    re_path(r'^faq$', FAQView.as_view(), name='faq_view'),
    path('faq/<int:pk>', FAQDetailView.as_view(), name='faq_detail_view'),
    path('faq/fields/', FAQFieldInfoView.as_view(), name='faq_fields_info'),
]
