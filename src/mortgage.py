from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import *
from reduce_type import ReduceType
from payment import Payment

class Mortgage(object):
    def __init__(self, schedule_calculator, loan, months, interest, date_given, early_repayments):
        self.months = months
        self.date_given = date_given
        self.first_payment_date = date_given + relativedelta(months=1)
        self.interest = interest
        self.early_repayments = early_repayments
        self.outstanding = []
        self.payments = []
        self.schedule_calculator = schedule_calculator
        self.outstanding.append(loan)
        self.__set_monthly_payment(months)
        self.schedule = []
        self.schedule = self.schedule_calculator.calculate(self, 0)

    def __set_monthly_payment(self, months_left):
        #M = P [ I ( 1 + I )^N ] / [ ( 1 + I )^N – 1 ]
        r = Decimal(self.interest / 12)
        interest_exp = pow((1 + r), months_left)
        ann = (r * interest_exp) / (interest_exp - 1)
        self.monthly_payment = Decimal(self.outstanding[-1] * ann)

    def make_monthly_payment(self, month, date):
        (principal, interest) = self.get_current_monthly_payment()
        return self.__make_payment(month, date, principal, interest, ReduceType.NONE)

    def get_current_monthly_payment(self):
        return self.get_monthly_payment(self.outstanding[-1])

    def get_monthly_payment(self, outstanding):
        interest = outstanding * Decimal(self.interest / 12)
        principal = self.pick_principal(outstanding, self.monthly_payment - interest)
        return (principal, interest)
    
    def __make_payment(self, month, date, principal, interest, reduce_type):
        paid = self.pick_principal(self.outstanding[-1], principal)
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
        
        if reduce_type == ReduceType.LENGTH:
            self.schedule = self.schedule_calculator.calculate(self, month_to_recalculate)
            self.months = len(self.schedule)
        elif reduce_type == ReduceType.PAYMENT:
            months_left = self.months - month_to_recalculate
            self.__set_monthly_payment(months_left)
            self.schedule = self.schedule_calculator.calculate(self, month_to_recalculate)
        return p
    
    def pick_principal(self, outstanding, principal):
        result = principal
        if principal > outstanding or abs(principal - outstanding) < 1:
            result = outstanding
        
        return result
