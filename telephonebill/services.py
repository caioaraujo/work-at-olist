from callrecord.models import CallRecord


class TelephoneBillService:

    def get_bill(self, phone, month, year):
        # TODO: Generate by month/year or last closed period
        return CallRecord.objects.filter(source=phone)
