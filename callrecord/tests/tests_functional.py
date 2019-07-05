from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from .fixtures import Fixtures


class CallStartRecordAPITests(APITestCase):

    @freeze_time('2012-01-02 12:44:59')
    def test_post__success(self):
        source = '9999999999'
        destination = '11111111111'

        data = {'source': source, 'destination': destination}
        response = self.client.post('/call-record/start/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data['data']
        self.assertTrue(obtained_data['id'] > 0)
        self.assertEqual(obtained_data['type'], 'START')
        self.assertEqual(obtained_data['source'], source)
        self.assertEqual(obtained_data['destination'], destination)

        timestamp = obtained_data['timestamp'].split('T')
        call_date = timestamp[0]
        self.assertEqual(call_date, '2012-01-02')
        call_time = timestamp[1]
        self.assertEqual(call_time, '12:44:59')

    def test_post__not_acceptable(self):
        data = {'destination': '1111111111'}
        response = self.client.post('/call-record/start/', data)

        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE,
                         response.status_code)
        self.assertEqual(response.data['detail'], 'Source is required')


class CallEndRecordAPITests(APITestCase):

    @freeze_time('2012-01-02 08:27:13')
    def test_post__success(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        source = '1111111111'
        destination = '2222222222'

        data = {'source': source, 'destination': destination}
        response = self.client.post('/call-record/end/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data['data']
        self.assertTrue(obtained_data['id'] > 0)
        self.assertEqual(obtained_data['type'], 'END')
        self.assertEqual(obtained_data['source'], source)
        self.assertEqual(obtained_data['destination'], destination)

        timestamp = obtained_data['timestamp'].split('T')
        call_date = timestamp[0]
        self.assertEqual(call_date, '2012-01-02')
        call_time = timestamp[1]
        self.assertEqual(call_time, '08:27:13')

    def test_post__not_acceptable(self):
        data = {'source': '1111111111', 'destination': '1111111111'}
        response = self.client.post('/call-record/end/', data)

        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE,
                         response.status_code)
        self.assertEqual(
            response.data['detail'],
            'Source and destination must be different')

    def test_post__internal_server_error(self):
        expected_error = ('Start record not found for source 9999999999 '
                          'and destination 1111111111')
        data = {'source': '9999999999', 'destination': '1111111111'}
        response = self.client.post('/call-record/end/', data)

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR,
                         response.status_code)
        self.assertEqual(response.data['detail'], expected_error)
