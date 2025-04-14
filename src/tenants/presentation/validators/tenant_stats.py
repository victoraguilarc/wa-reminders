# -*- coding: utf-8 -*-


from rest_framework import serializers

class DailyMetricsValidator(serializers.Serializer):
    from_date = serializers.DateField(required=True)
    to_date = serializers.DateField(required=True)
