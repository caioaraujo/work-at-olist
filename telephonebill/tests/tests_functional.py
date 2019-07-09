from rest_framework import status
from rest_framework.test import APITestCase


class TelephoneBillAPITests(APITestCase):

    def test_get__no_data_found(self):
        source = '9999999999'
        response = self.client.get(f'/telephone-bill/{source}/')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get__no_filter(self):
        pass
        # source = '11111111111'
        # response = self.client.get(f'/telephone-bill/{source}/')
        #
        # self.assertEqual(status.HTTP_200_OK, response.status_code)
