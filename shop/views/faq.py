
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restapp.pagination import ResultsSetPagination

from shop.filterset import FAQFilter
from shop.models import FAQ
from shop.serializers import FAQListSerializer, FAQSerializer


class FAQFieldInfoView(APIView):
    """
    Admin uchun – model fieldlar haqida metadata (DistrictFieldInfoView shabloni).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        field_info = []
        for field in FAQ._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None,
            })
        return Response(field_info)


class FAQView(ListCreateAPIView):
    """
    FAQ (Часто задаваемые вопросы) bo‘limi uchun model.
        - question: savol matni
        - answer: javob matni (HTML bo‘lishi ham mumkin)
        - order: tartiblash uchun
        - is_active: faqat aktivlari front va botga beriladi
    """
    serializer_class = FAQListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = FAQFilter
    search_fields = ('question', 'answer', 'category')
    ordering = ['order', 'pk']

    def get_queryset(self):
        return FAQ.objects.all()

    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # BaseModel’da created_by bo‘lsa – shuni ishlatyapmiz
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FAQDetailView(RetrieveUpdateDestroyAPIView):
    """
    Bitta FAQ elementini ko‘rish / tahrirlash / o‘chirish.
    DistrictDetailView shabloniga mos.
    """
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(FAQ, id=pk)
        serializer = FAQListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(FAQ, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
