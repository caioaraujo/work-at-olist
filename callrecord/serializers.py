from rest_framework import serializers

from .models import CallRecord


class CallStartRecordSerializer(serializers.ModelSerializer):

    source = serializers.CharField(help_text='Source phone number',
                                   required=True,
                                   max_length=11)
    destination = serializers.CharField(help_text='Destination phone number',
                                        required=True,
                                        max_length=11)

    class Meta:
        model = CallRecord
        fields = ('id', 'type', 'timestamp', 'call_id', 'source',
                  'destination')
        read_only_fields = ('id', 'type', 'timestamp', 'call_id')
