from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import CallStartRecordSerializer
from .services import CallRecordService


class CallStartRecordView(GenericAPIView):
    serializer_class = CallStartRecordSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TYPE = 'START'

    def post(self, request):
        """
        Save a call start record.
        """

        # Extract all request parameters
        request_data = request.data
        source = request_data['source']
        destination = request_data['destination']

        data = CallRecordService().insert(self.TYPE, source, destination)
        serializer = CallStartRecordSerializer(data)

        result = {'detail': 'Call start recorded successfully!',
                  'data': serializer.data}
        return Response(result)
