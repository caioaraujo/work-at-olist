import time
from datetime import datetime, timedelta

from .models import TelephoneBill


class TelephoneBillService:
    STANDING_CHARGE = 0.36
    CHARGE_MINUTE = 0.09

    def save_telephone_bill(self, source, destination, timestamp_start,
                            timestamp_end):
        """
        Save a telephone bill record between a call start and a call end

        Args:
            source: source phone number
            destination: destination phone number
            timestamp_start: datetime from the call start
            timestamp_end: datetime from the call end

        Returns: TelephoneBill model instance

        """
        call_price = self._calculate_call_price(timestamp_start, timestamp_end)
        call_duration = self._calculate_call_duration(
            timestamp_start, timestamp_end)

        telephone_bill = TelephoneBill(
            source=source, destination=destination, call_price=call_price,
            call_start_date=timestamp_start.date(),
            call_start_time=timestamp_start.time(),
            year=timestamp_start.year, month=timestamp_start.month,
            call_duration=call_duration
        )

        telephone_bill.save()

        return telephone_bill

    def _calculate_call_duration(self, timestamp_start, timestamp_end):
        """
        Calculate the call duration

        Args:
            timestamp_start: datetime from the call start
            timestamp_end: datetime from the call end

        Returns: time elapsed as time

        """

        # Get the difference between both datetime
        difference = timestamp_end - timestamp_start

        # Extract the time part from the timedelta object
        diff_time = (datetime.min + difference).time()

        # Calculate the amount of hours
        total_hours = diff_time.hour + difference.days * 24

        # Format all time values before return it
        total_hours = str(total_hours).zfill(2)
        total_minutes = str(diff_time.minute).zfill(2)
        total_seconds = str(diff_time.second).zfill(2)

        return f"{total_hours}:{total_minutes}:{total_seconds}"

    def _calculate_call_price(self, timestamp_start, timestamp_end):
        """
        Calculate the call price

        Args:
            timestamp_start: datetime from the call start
            timestamp_end: datetime from the call end

        Returns: The price in float

        """

        # Find the total of minutes between these dates
        diff_time = timestamp_end - timestamp_start
        total_minutes = diff_time.seconds // 60

        # Set zero to seconds from both dates
        timestamp_start = self._set_zero_to_seconds(timestamp_start)
        timestamp_end = self._set_zero_to_seconds(timestamp_end)

        while timestamp_start <= timestamp_end:

            if timestamp_start.hour > 21 or timestamp_start.hour < 6:
                # Removes the minute if the interval is between
                # the non-charged time (22h00 and 5h59)
                total_minutes -= 1
            # Increment one minute do timestamp_start
            timestamp_start = timestamp_start + timedelta(minutes=1)

        price = total_minutes * self.CHARGE_MINUTE + self.STANDING_CHARGE
        return round(price, ndigits=2)

    def _set_zero_to_seconds(self, timestamp):
        return timestamp.replace(second=0, microsecond=0)

    def get_telephone_bill(self, phone, month, year):
        # FIXME
        return TelephoneBill.objects.all()