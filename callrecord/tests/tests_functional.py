from rest_framework import status
from rest_framework.test import APITestCase


class CallStartRecordAPITests(APITestCase):

    def test_post__success(self):
        source = '9999999'
        destination = '1111111'

        data = {'source': source, 'destination': destination}
        response = self.client.post('/call-record/start/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
