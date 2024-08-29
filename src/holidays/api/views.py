import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from holidays.api.filterset import HolidayFilterSet
from holidays.api.serializers import HolidaySerializer, HolidayDatatableSerializer

class ListHolidaysView(ListAPIView):
    serializer_class = HolidaySerializer

    def get_queryset(self):
        url = 'https://date.nager.at/api/v3/PublicHolidays/2024/CR'
        response = requests.get(url)
        return response.json()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.paginate_queryset(queryset)
        response = {
            'data': data,
            'recordsTotal': len(queryset),
            'recordsFiltered': len(queryset),
            'draw': self.request.GET.get('draw', 1)
        }
        return Response(HolidayDatatableSerializer(response).data)


# class HolidaysApiView(APIView):
#     def get(self, request):
#         url = 'https://date.nager.at/api/v3/PublicHolidays/2024/CR'
#
#         response = requests.get(url)
#         data = response.json()
#
#         serializer = HolidaySerializer(data=data, many=True)
#         serializer.is_valid()
#         return Response(serializer.data)
