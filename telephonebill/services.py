from datetime import datetime, date, timedelta

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
            year=timestamp_end.year, month=timestamp_end.month,
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

        Returns: time elapsed as string (eg 35:23:07)

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

        # Transfer the past seconds from start timestamp to the
        # end timestamp before count all minutes between then
        start_seconds = 60 - timestamp_start.second
        timestamp_end = timestamp_end + timedelta(seconds=start_seconds)
        timestamp_start = timestamp_start + timedelta(seconds=start_seconds)

        # Find the total of minutes between these dates
        diff_time = timestamp_end - timestamp_start
        total_minutes = diff_time.seconds // 60

        timestamp_end = self._set_zero_to_seconds(timestamp_end)

        non_charged_minutes = sum(self._generate_non_charged_minutes(
            timestamp_start, timestamp_end))
        total_minutes = total_minutes - non_charged_minutes

        price = total_minutes * self.CHARGE_MINUTE + self.STANDING_CHARGE
        return round(price, ndigits=2)

    def _generate_non_charged_minutes(self, timestamp_start, timestamp_end):
        # Generates all minutes in the non-charged interval (22h00 and 5h59)

        while timestamp_start < timestamp_end:
            start_hour = timestamp_start.hour

            if (timestamp_start.date() == timestamp_end.date() and
                    start_hour == timestamp_end.hour):
                # If the hour is the same, the amount of left minutes
                # is the difference between end and start minutes
                minutes = timestamp_end.minute - timestamp_start.minute

            else:
                minutes = 60 - timestamp_start.minute

            if start_hour > 21 or start_hour < 6:
                yield minutes
            # Add these minutes to timestamp_start
            timestamp_start = timestamp_start + timedelta(minutes=minutes)

    def _set_zero_to_seconds(self, timestamp):
        return timestamp.replace(second=0, microsecond=0)

    def get_telephone_bill(self, phone, month, year):

        period = self._get_period_filter(month, year)

        return TelephoneBill.objects.filter(source=phone, **period)

    def _get_period_filter(self, month, year):
        # Return the period filter

        period = {'year': self._get_year_filter(month, year)}

        if month:
            period['month'] = month

        if not month and not year:
            # Month and year were not sent.
            # In this case find the last month data

            previous_month = self._get_date_from_previous_month()

            period['month'] = previous_month.month
            period['year'] = previous_month.year

        return period

    def _get_year_filter(self, month, year):
        if year:
            return year

        if month:
            # Month was sent, but not year.
            # In this case get the year related to
            # the last occurrence of the given month

            current_day = date.today()
            if int(month) > current_day.month:
                return current_day.year - 1
            return current_day.year

    def _get_date_from_previous_month(self):
        # Find the previous month date related to the first day of the
        # current month
        current_day = date.today()
        first_day_of_current_month = current_day.replace(day=1)
        return first_day_of_current_month - timedelta(days=1)
