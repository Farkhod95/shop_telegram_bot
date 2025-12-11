from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from shop.filterset import PointsTransactionFilter
from shop.models import PointsTransaction
from shop.serializers import PointsTransactionListSerializer, PointsTransactionSerializer


class PointsTransactionFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in PointsTransaction._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class PointsTransactionView(ListCreateAPIView):
    """
    Ball balansidagi o‘zgarishlar tarixi (ledger).
        - Har qanday ball qo‘shish / ayirish shu yerda yoziladi:
          QR skan, market xarid, rozigrishda ishtirok, referal bonusi, profilni to‘ldirish va h.k.
        - amount: ijobiy bo‘lsa ball qo‘shiladi, manfiy bo‘lsa balansdan ayriladi.
        - reason: ball nimaga berilganini aniq ko‘rsatish (hisob-kitob va audit uchun).
        UIda “b 0” ikonkasini ko‘rsatish, balansni qayta hisoblash, istoriyani chiqarish uchun asosiy model.
    """

    serializer_class = PointsTransactionListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = PointsTransactionFilter
    ordering = ['-id']

    def get_queryset(self):
        return PointsTransaction.objects.all()

    def post(self, request):
        serializer = PointsTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PointsTransactionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PointsTransactionSerializer

    def get_queryset(self):
        return PointsTransaction.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(PointsTransaction, id=pk)
        serializer = PointsTransactionListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(PointsTransaction, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
