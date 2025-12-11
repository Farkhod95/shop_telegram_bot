from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from shop.filterset import CartFilter
from shop.models import Cart
from shop.serializers import CartListSerializer, CartSerializer


class CartFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in Cart._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class CartView(ListCreateAPIView):
    """
    Foydalanuvchining savatchasi (Корзина).
        - Har bir BurnUser uchun bir nechta cart bo‘lishi mumkin (ochiq, yakunlangan va h.k.).
        - total_points – savatchadagi mahsulotlar umumiy ball narxi (balansni tekshirish uchun).
        - Telegram botda katalogdan “В корзину” bosilganda CartItem lar shu yerga yig‘iladi.
    """
    serializer_class = CartListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = CartFilter
    ordering = ['pk']

    def get_queryset(self):
        return Cart.objects.all()

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(Cart, id=pk)
        serializer = CartListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(Cart, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
