from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from directory.filterset import ProductSizeFilter
from directory.models import ProductSize
from directory.serializers import ProductSizeListSerializer, ProductSizeSerializer


class ProductSizeFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in ProductSize._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class ProductSizeView(ListCreateAPIView):
    """
    Mahsulot o‘lchamlari: S, M, L, XL va hokazo.
        Har bir Product bir nechta size’ga ega bo‘lishi mumkin.
    """

    serializer_class = ProductSizeListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = ProductSizeFilter
    search_fields = ('label',)
    ordering = ['order', 'pk']

    def get_queryset(self):
        return ProductSize.objects.all()

    def post(self, request):
        serializer = ProductSizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductSizeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSizeSerializer

    def get_queryset(self):
        return ProductSize.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(ProductSize, id=pk)
        serializer = ProductSizeListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(ProductSize, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
