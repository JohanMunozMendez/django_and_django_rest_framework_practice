from django.urls import path

from holidays.api.views import ListHolidaysView, HolidaysApiView
from holidays.views import holidays_list

app_name = 'holidays'

urlpatterns = [
    # path('holidays/', HolidaysApiView.as_view(), name='holidays'),
    path('list_holidays/', ListHolidaysView.as_view(), name='apiview_holidays'),
    path('holidays_list/', holidays_list, name='holidays_list'),
]