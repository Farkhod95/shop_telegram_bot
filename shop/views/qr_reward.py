from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from shop.filterset import QRRewardFilter
from shop.models import QRReward
from shop.serializers import QRRewardListSerializer, QRRewardSerializer


class QRRewardFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in QRReward._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class QRRewardView(ListCreateAPIView):
    """
    QR kod / havola orqali beriladigan mukofot konfiguratsiyasi.
        - code: QR ichidagi token yoki link parametri (unikal).
        - points: bir marta skan qilinganda beriladigan ball.
        - max_uses / used_count: umumiy necha marta ishlatilishi mumkinligini cheklash.
        - is_active: QR hozir aktivmi yoki bloklangan.
        4-rasmdagi “Сканируй QR-коды, получай баллы” logikasini backendda ta’minlaydi.
    """

    serializer_class = QRRewardListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = QRRewardFilter
    search_fields = ('code',)
    ordering = ['pk']

    def get_queryset(self):
        return QRReward.objects.all()

    def post(self, request):
        serializer = QRRewardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QRRewardDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = QRRewardSerializer

    def get_queryset(self):
        return QRReward.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(QRReward, id=pk)
        serializer = QRRewardListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(QRReward, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
