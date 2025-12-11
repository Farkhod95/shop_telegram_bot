from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from shop.filterset import ProductFilter
from shop.models import Product
from shop.serializers import ProductListSerializer, ProductSerializer


class ProductFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in Product._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class ProductView(ListCreateAPIView):
    """
    Market va Розыгрышdagi barcha obyektlar (futbolka, huddi, krossovka, iPhone va h.k.).
        - type:
            MARKET  – oddiy market, tugma “В корзину”, Cart orqali sotib olinadi.
            RAFFLE – розыгрыш, tugma “Играть”, foydalanuvchi ball sarflab o‘yin o‘ynaydi.
        - price_points / old_price_points – hozirgi va eski ball narxi (chegirma ko‘rsatish uchun).
        - sizes / is_one_size – o‘lchamlar bilan ishlash (“Размер” / “Один размер” selectlari).
        - stock, is_limited, is_active – ombor va aktivlik nazorati.
    """
    serializer_class = ProductListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = ProductFilter
    search_fields = ('title', 'subtitle')
    ordering = ['pk']

    def get_queryset(self):
        return Product.objects.all()

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(Product, id=pk)
        serializer = ProductListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(Product, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
