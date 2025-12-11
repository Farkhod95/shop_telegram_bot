from django.urls import re_path, path

from .views.country import CountryView, CountryDetailView, CountryFieldInfoView
from .views.district import DistrictView, DistrictDetailView, DistrictFieldInfoView
from .views.import_country import CountryFileImportView
from .views.product_category import ProductCategoryView, ProductCategoryDetailView, ProductCategoryFieldInfoView
from .views.product_size import ProductSizeView, ProductSizeDetailView, ProductSizeFieldInfoView
from .views.region import RegionView, RegionDetailView, RegionFieldInfoView

urlpatterns = [
    re_path(r'^country$', CountryView.as_view(), name='country_view'),
    path('country/<int:pk>', CountryDetailView.as_view(), name='country_detail_view'),
    path('country/fields/', CountryFieldInfoView.as_view(), name='country_fields_info'),
    path("country/import-from-file/", CountryFileImportView.as_view(),
             name="country-import-from-file"),

    re_path(r'^region$', RegionView.as_view(), name='regions_view'),
    path('region/<int:pk>', RegionDetailView.as_view(), name='region_detail_view'),
    path('region/fields/', RegionFieldInfoView.as_view(), name='region_fields_info'),

    re_path(r'^district$', DistrictView.as_view(), name='districts_view'),
    path('district/<int:pk>', DistrictDetailView.as_view(), name='districts_detail_view'),
    path('district/fields/', DistrictFieldInfoView.as_view(), name='district_fields_info'),

    # ProductCategory
    re_path(r'^product-categories$', ProductCategoryView.as_view(), name='product_categories_view'),
    path('product-categories/<int:pk>', ProductCategoryDetailView.as_view(), name='product_categories_detail_view'),
    path('product-categories/fields/', ProductCategoryFieldInfoView.as_view(), name='product_categories_fields_info'),

    # ProductSize
    re_path(r'^product-sizes$', ProductSizeView.as_view(), name='product_sizes_view'),
    path('product-sizes/<int:pk>', ProductSizeDetailView.as_view(), name='product_sizes_detail_view'),
    path('product-sizes/fields/', ProductSizeFieldInfoView.as_view(), name='product_sizes_fields_info'),

]