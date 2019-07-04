from django.test import TestCase

from ..services import CallRecordService
from .fixtures import Fixtures


class TestCallRecordService(TestCase):

    def test_get_call_id__first_database_record(self):
        service = CallRecordService()
        call_record_type = 'START'
        source = '2222222'
        destination = '111111'

        call_id = service._get_call_id(call_record_type, source, destination)
        self.assertEqual(1, call_id)

    def test_get_call_id__call_type_start(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        service = CallRecordService()
        call_record_type = 'START'
        source = '22222'
        destination = '11111'

        call_id = service._get_call_id(call_record_type, source, destination)
        self.assertEqual(21, call_id)

    def test_get_call_id__call_type_stop(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        service = CallRecordService()
        call_record_type = 'STOP'
        source = '11111'
        destination = '22222'

        call_id = service._get_call_id(call_record_type, source, destination)
        self.assertEqual(9, call_id)
