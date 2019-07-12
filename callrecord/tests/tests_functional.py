from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from telephonebill.models import TelephoneBill
from .fixtures import Fixtures


class CallStartRecordAPITests(APITestCase):

    def test_post__success(self):
        source = '9999999999'
        destination = '11111111111'
        call_id = 33
        timestamp = '2016-02-29T12:00:00Z'

        data = {'source': source, 'destination': destination,
                'call_id': call_id, 'timestamp': timestamp}
        response = self.client.post('/call-record/start/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data['data']
        self.assertTrue(obtained_data['id'] > 0)
        self.assertEqual(obtained_data['type'], 'START')
        self.assertEqual(obtained_data['source'], source)
        self.assertEqual(obtained_data['destination'], destination)
        self.assertEqual(obtained_data['call_id'], call_id)

        timestamp_response = datetime.strptime(
            obtained_data['timestamp'], '%Y-%m-%d %H:%M:%S')

        self.assertEqual(timestamp_response, datetime(2016, 2, 29, 12, 0, 0))

    def test_post__not_acceptable(self):
        data = {'destination': '1111111111'}
        response = self.client.post('/call-record/start/', data)

        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE,
                         response.status_code)
        self.assertEqual(response.data['detail'], 'Source is required')


class CallEndRecordAPITests(APITestCase):

    def test_post__success(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        call_id = 9
        timestamp = '2012-01-02T08:27:13Z'

        data = {'call_id': call_id, 'timestamp': timestamp}
        response = self.client.post('/call-record/end/', data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Assert response data
        obtained_data = response.data['data']
        self.assertTrue(obtained_data['id'] > 0)
        self.assertEqual(obtained_data['type'], 'END')
        self.assertEqual(obtained_data['source'], '1111111111')
        self.assertEqual(obtained_data['destination'], '2222222222')
        self.assertEqual(obtained_data['call_id'], 9)

        timestamp_response = datetime.strptime(
            obtained_data['timestamp'], '%Y-%m-%d %H:%M:%S')

        self.assertEqual(timestamp_response, datetime(2012, 1, 2, 8, 27, 13))

        # Asserting the telephone bill
        telephone_bill = (TelephoneBill.objects
                          .filter(source='1111111111',
                                  destination='2222222222'))
        self.assertTrue(telephone_bill.exists())
        telephone_bill = telephone_bill.first()
        self.assertEqual(str(telephone_bill.call_price), '13.59')
        self.assertEqual(telephone_bill.call_duration, '03:15:54')
        self.assertEqual(telephone_bill.year, 2012)
        self.assertEqual(telephone_bill.month, 1)

        expected_start_date = datetime(2012, 1, 2, 5, 11, 19)
        self.assertEqual(
            telephone_bill.call_start_date, expected_start_date.date())
        self.assertEqual(
            telephone_bill.call_start_time, expected_start_date.time())

    def test_post__not_acceptable(self):
        data = {'timestamp': '2012-01-02T08:27:13Z'}
        response = self.client.post('/call-record/end/', data)

        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE,
                         response.status_code)
        self.assertEqual(
            response.data['detail'],
            'Call id is required')

    def test_post__internal_server_error(self):
        expected_error = 'Start record not found for call id 99'
        data = {'call_id': 99, 'timestamp': '2012-01-02T08:27:13Z'}
        response = self.client.post('/call-record/end/', data)

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR,
                         response.status_code)
        self.assertEqual(response.data['detail'], expected_error)
