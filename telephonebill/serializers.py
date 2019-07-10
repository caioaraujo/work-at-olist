from rest_framework import serializers

from .models import TelephoneBill


class TelephoneBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelephoneBill
        fields = (
            'destination', 'call_start_date', 'call_start_time',
            'call_duration', 'call_price', )
