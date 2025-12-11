from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from shop.filterset import QRTutorialSlideFilter
from shop.models import QRTutorialSlide
from shop.serializers import QRTutorialSlideListSerializer, QRTutorialSlideSerializer


class QRTutorialSlideFieldInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in QRTutorialSlide._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class QRTutorialSlideView(ListCreateAPIView):
    """
    “Как сканировать QR-код?” bo‘limidagi slaydlar (1/4, 2/4, 3/4, 4/4).
        - Har bir slayd uchun sarlavha, matn va rasm saqlanadi.
        - order bo‘yicha tartiblanadi.
        Frontda foydalanuvchiga QR skan qilish bo‘yicha vizual instruktsiya ko‘rsatish uchun.
    """

    serializer_class = QRTutorialSlideListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = QRTutorialSlideFilter
    search_fields = ('title',)
    ordering = ['order', 'pk']

    def get_queryset(self):
        return QRTutorialSlide.objects.all()

    def post(self, request):
        serializer = QRTutorialSlideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QRTutorialSlideDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = QRTutorialSlideSerializer

    def get_queryset(self):
        return QRTutorialSlide.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(QRTutorialSlide, id=pk)
        serializer = QRTutorialSlideListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(QRTutorialSlide, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
