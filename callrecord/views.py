from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import CallRecordStartSerializer, CallRecordEndSerializer
from .services import CallRecordService


class CallStartRecordView(GenericAPIView):
    serializer_class = CallRecordStartSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        """
        Save a call start record.
        """

        # Extract all request parameters
        request_data = request.data
        source = request_data.get('source')
        destination = request_data.get('destination')
        call_id = request_data.get('call_id')
        timestamp = request_data.get('timestamp')

        data = CallRecordService().insert_call_start(
            source, destination, call_id, timestamp)
        serializer = CallRecordStartSerializer(data)

        result = {'detail': 'Call start recorded successfully!',
                  'data': serializer.data}
        return Response(result)


class CallEndRecordView(GenericAPIView):
    serializer_class = CallRecordEndSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        """
        Save a call end record.
        """

        # Extract all request parameters
        request_data = request.data
        call_id = request_data.get('call_id')
        timestamp = request_data.get('timestamp')

        service = CallRecordService()

        # Save the call record
        data = service.insert_call_end(call_id, timestamp)

        serializer = CallRecordEndSerializer(data)

        result = {'detail': 'Call end recorded successfully!',
                  'data': serializer.data}
        return Response(result)
