from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import CallRecordSerializer
from .services import CallRecordService


class CallStartRecordView(GenericAPIView):
    serializer_class = CallRecordSerializer

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

        data = CallRecordService().insert_call_start(source, destination)
        serializer = CallRecordSerializer(data)

        result = {'detail': 'Call start recorded successfully!',
                  'data': serializer.data}
        return Response(result)


class CallEndRecordView(GenericAPIView):
    serializer_class = CallRecordSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        """
        Save a call end record.
        """

        # Extract all request parameters
        request_data = request.data
        source = request_data.get('source')
        destination = request_data.get('destination')

        service = CallRecordService()

        # Save the call record
        data = service.insert_call_end(source, destination)

        serializer = CallRecordSerializer(data)

        result = {'detail': 'Call end recorded successfully!',
                  'data': serializer.data}
        return Response(result)
