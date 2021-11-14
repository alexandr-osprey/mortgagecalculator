from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import *
from reduce_type import ReduceType
from payment import Payment

class Mortgage(object):
    def __init__(self, schedule_calculator, loan, months, interest, first_payment_date, early_repayments):
        self.months = months
        self.first_payment_date = first_payment_date
        self.interest = interest
        self.early_repayments = early_repayments
        self.outstanding = []
        self.payments = []
        self.schedule_calculator = schedule_calculator
        self.outstanding.append(loan)
        self.__set_monthly_payment()
        self.schedule = []
        self.schedule = self.schedule_calculator.calculate(self, 0)

    def __set_monthly_payment(self):
        #M = P [ I ( 1 + I )^N ] / [ ( 1 + I )^N – 1 ]
        r = Decimal(self.interest / 12)
        interest_exp = pow((1 + r), self.months)
        ann = (r * interest_exp) / (interest_exp - 1)
        self.monthly_payment = Decimal(self.outstanding[-1] * ann)

    def make_monthly_payment(self, month, date):
        (principal, interest) = self.get_monthly_payment()
        return self.__make_payment(month, date, principal, interest, ReduceType.NONE)

    def get_monthly_payment(self):
        interest = self.outstanding[-1] * Decimal(self.interest / 12)
        principal = self.monthly_payment - interest
        return (principal, interest)
    
    def __make_payment(self, month, date, principal, interest, reduce_type):
        paid = principal
        if abs(principal - self.outstanding[-1]) < 1:
            paid = self.outstanding[-1]
        o = self.outstanding[-1] - paid
        self.outstanding.append(o)
        p = Payment(paid, interest, date, o)
        self.payments.append(p)
        return p

    def make_early_payment(self, month, date, principal, reduce_type):
        p = self.__make_payment(month, date, principal, 0, reduce_type)
        after_date =  date.day >= self.first_payment_date.day
        if after_date:
            month_to_recalculate = month + 1
        else:
            month_to_recalculate = month
        
        self.schedule = self.schedule_calculator.calculate(self, month_to_recalculate)
        self.months = len(self.schedule)
        return p
