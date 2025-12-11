from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from shop.filterset import QRScanHistoryFilter
from shop.models import QRScanHistory
from shop.serializers import QRScanHistoryListSerializer, QRScanHistorySerializer


class QRScanHistoryFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in QRScanHistory._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class QRScanHistoryView(ListCreateAPIView):
    """
    Foydalanuvchilarning QR kodlarni skan qilish tarixi.
        - Har bir skan uchun user, qaysi QRReward, necha ball berildi va vaqtini yozib boradi.
        - Statistikalar, antifraud va support uchun kerak bo‘ladi (“sen bu QRni allaqachon ishlatgansan” va h.k.).
    """

    serializer_class = QRScanHistoryListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = QRScanHistoryFilter
    ordering = ['-scanned_at']

    def get_queryset(self):
        return QRScanHistory.objects.all()

    def post(self, request):
        serializer = QRScanHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QRScanHistoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = QRScanHistorySerializer

    def get_queryset(self):
        return QRScanHistory.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(QRScanHistory, id=pk)
        serializer = QRScanHistoryListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(QRScanHistory, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
