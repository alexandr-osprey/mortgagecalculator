from schedule_calculator import ScheduleCalculator
from payment import Payment
from mortgage import Mortgage
from unittest.mock import  Mock, MagicMock, PropertyMock
from unittest import TestCase
import unittest
import datetime
from decimal import *

class TestScheduleCalculator(TestCase):
    
    
    def test_calculate_12_months(self):
        calculator = ScheduleCalculator()
        self.monthly_payment = Decimal(888.49)
        self.interest = 0.12
        mortgage = MagicMock(spec=Mortgage)
        type(mortgage).outstanding = PropertyMock(return_value=[10000])
        type(mortgage).schedule = PropertyMock(return_value=[])
        mortgage.get_monthly_payment = self.get_monthly_payment
        months = 12
        type(mortgage).months = PropertyMock(return_value=months)
        type(mortgage).first_payment_date = PropertyMock(return_value=datetime.datetime(2020, 1, 1))

        schedule = calculator.calculate(mortgage, 0)

        self.assertEqual(months, len(schedule))
        self.assertEqual(0, schedule[-1].balance)
    
    def get_monthly_payment(self, outstanding):
        interest = outstanding * Decimal(self.interest / 12)
        principal = self.monthly_payment - interest
        return (principal, interest)



if __name__ == '__main__':
    unittest.main()
