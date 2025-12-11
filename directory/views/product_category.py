from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from directory.filterset import ProductCategoryFilter
from directory.models import ProductCategory
from directory.serializers import ProductCategoryListSerializer, ProductCategorySerializer


class ProductCategoryFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in ProductCategory._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class ProductCategoryView(ListCreateAPIView):
    """
    Market va Розыгрыш bo‘limlaridagi mahsulot kategoriyalari.
        Masalan: Hit, Burn, Overdose, Banger.
        Frontda blok sarlavhasi sifatida chiqadi, tartib order bo‘yicha boshqariladi.
    """

    serializer_class = ProductCategoryListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = ProductCategoryFilter
    search_fields = ('name', 'slug')
    ordering = ['order', 'pk']

    def get_queryset(self):
        return ProductCategory.objects.all()

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductCategoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        return ProductCategory.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(ProductCategory, id=pk)
        serializer = ProductCategoryListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(ProductCategory, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
