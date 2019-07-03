from rest_framework.response import Response
from rest_framework.views import APIView


class CallStartRecordView(APIView):

    def post(self, request):
        return Response("OK")
