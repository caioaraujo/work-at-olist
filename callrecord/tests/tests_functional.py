from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase


class CallStartRecordAPITests(APITestCase):

    @freeze_time('2012-01-02 08:27')
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

        call_timestamp = obtained_data['timestamp'].split('T')[0]
        self.assertEqual(call_timestamp, '2012-01-02')

    def test_post__not_acceptable(self):
        data = {'destination': '1111111111'}
        response = self.client.post('/call-record/start/', data)

        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE,
                         response.status_code)
        self.assertEqual(response.data['detail'], 'Source is required')
