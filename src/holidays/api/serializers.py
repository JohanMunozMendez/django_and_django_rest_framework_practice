import datetime

from rest_framework import serializers


class HolidaySerializer(serializers.Serializer):
    name = serializers.CharField()
    date = serializers.DateField()
    day_of_week = serializers.SerializerMethodField()
    countryCode = serializers.CharField()

    def get_day_of_week(self, obj):
        return datetime.datetime.strptime(obj['date'], '%Y-%m-%d').strftime('%A')

class HolidayDatatableSerializer(serializers.Serializer):
    data = serializers.ListField(child=HolidaySerializer(), required=True)
    draw = serializers.IntegerField(required=True)
    recordsFiltered = serializers.IntegerField(required=True)
    recordsTotal = serializers.IntegerField(required=True)