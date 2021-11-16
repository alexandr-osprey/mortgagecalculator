from schedule_calculator import ScheduleCalculator
from mortgage import Mortgage
from unittest.mock import  Mock, MagicMock, PropertyMock
from unittest import TestCase
import unittest
import datetime

class TestScheduleCalculator(TestCase):
    def test_calculate_one_month(self):
        calculator = ScheduleCalculator()
        mortgage = MagicMock(spec=Mortgage)
        type(mortgage).outstanding = PropertyMock(return_value=[1000])
        type(mortgage).schedule = PropertyMock(return_value=[])
        mortgage.get_monthly_payment = MagicMock(return_value=(1000, 100))
        m = PropertyMock(return_value=1)
        type(mortgage).months = m
        type(mortgage).first_payment_date = PropertyMock(return_value=datetime.datetime(2020, 1, 1))

        schedule = calculator.calculate(mortgage, 0)

        self.assertEqual(1, len(schedule))
        self.assertEqual(1, len(schedule))

if __name__ == '__main__':
    unittest.main()