from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from app_warehouse.filters import ShipmentFilter
from app_warehouse.models import Shipment, Loading
from app_warehouse.serializers import ShipmentSerializer, LoadingSerializer


class ShipmentListApi(ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    # pagination_class = ShipmentPagination
    # permission_classes = [IsAdminUser]


class ShipmentDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAdminUser]


class LoadingListApi(ListCreateAPIView):
    queryset = Loading.objects.all()
    serializer_class = LoadingSerializer
    permission_classes = [IsAdminUser]


class LoadingDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Loading.objects.all()
    serializer_class = LoadingSerializer
    permission_classes = [IsAdminUser]


class ShipmentListView(ListView):
    template_name = 'shipment_list.html'
    model = Shipment

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShipmentListView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        filtered_shipments_qs = ShipmentFilter(self.request.GET, queryset=Shipment.objects.all()).qs
        paginator = Paginator(filtered_shipments_qs, 20)
        try:
            filtered_shipments = paginator.page(page)
        except PageNotAnInteger:
            filtered_shipments = paginator.page(1)
        except EmptyPage:
            filtered_shipments = paginator.page(paginator.num_pages)
        context['object_list'] = filtered_shipments
        return context

