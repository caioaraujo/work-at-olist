from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from .filters import TelephoneBillFilterBackend
from .serializers import TelephoneBillSerializer
from .services import TelephoneBillService


class TelephoneBillView(GenericAPIView, ListModelMixin):
    """
    Services for phone number billing
    """

    filter_backends = [TelephoneBillFilterBackend, ]
    serializer_class = TelephoneBillSerializer

    def get(self, request, phone):
        """
        Returns a list of the call billing of the number,
        by month and/or year. By default it will returns
        the billet from the last closed period (month)
        """
        service = TelephoneBillService()
        month = request.GET.get('month')
        year = request.GET.get('year')

        data = service.get_bill(phone, month, year)
        serializer = TelephoneBillSerializer(data, many=True)

        return Response(serializer.data)
