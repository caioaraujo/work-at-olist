from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from .fixtures import Fixtures


class TelephoneBillAPITests(APITestCase):

    def test_get__no_data_found(self):
        source = '9999999999'
        response = self.client.get(f'/telephone-bill/{source}/')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    @freeze_time('2018-06-02')
    def test_get__no_filter(self):
        # Install fixtures
        Fixtures.create_telephone_bill_fixtures()

        source = '11111111111'
        response = self.client.get(f'/telephone-bill/{source}/')

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data
        self.assertEqual(2, len(obtained_data))

        total_price = self._get_total_price(obtained_data)
        self.assertEqual(0.74, total_price)

    @freeze_time('2019-03-02')
    def test_get__by_month(self):
        # Install fixtures
        Fixtures.create_telephone_bill_fixtures()

        source = '11111111111'
        month = 4

        data = {'month': month}
        response = self.client.get(f'/telephone-bill/{source}/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data
        self.assertEqual(1, len(obtained_data))

        total_price = self._get_total_price(obtained_data)
        self.assertEqual(12.66, total_price)

    @freeze_time('2019-03-02')
    def test_get__by_year(self):
        # Install fixtures
        Fixtures.create_telephone_bill_fixtures()

        source = '11111111111'
        year = 2018

        data = {'year': year}
        response = self.client.get(f'/telephone-bill/{source}/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data
        self.assertEqual(4, len(obtained_data))

        total_price = self._get_total_price(obtained_data)
        self.assertEqual(13.79, total_price)

    @freeze_time('2019-03-02')
    def test_get__by_month_and_year(self):
        # Install fixtures
        Fixtures.create_telephone_bill_fixtures()

        source = '11111111111'
        month = 5
        year = 2018

        data = {'month': month, 'year': year}
        response = self.client.get(f'/telephone-bill/{source}/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data
        self.assertEqual(2, len(obtained_data))

        total_price = self._get_total_price(obtained_data)
        self.assertEqual(0.74, total_price)

    def _get_total_price(self, data):
        return sum([float(x['call_price']) for x in data])
