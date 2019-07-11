import coreapi
import coreschema
from rest_framework.filters import BaseFilterBackend


class TelephoneBillFilterBackend(BaseFilterBackend):
    """ Filter fields for search engine """

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='month',
                required=False,
                schema=coreschema.Integer(
                    description='The reference month number [1-12]'),
                location='query',
                type=int,
            ),
            coreapi.Field(
                name='year',
                required=False,
                schema=coreschema.Integer(
                    description='The reference year number (eg 2018)'),
                location='query',
                type=int,
            ),
        ]
