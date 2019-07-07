from rest_framework import serializers

from callrecord.models import CallRecord


class TelephoneBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallRecord
        fields = '__all__'
