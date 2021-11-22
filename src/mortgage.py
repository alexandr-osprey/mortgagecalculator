from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import *
from reduce_type import ReduceType
from paid_entry import PaidEntry

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
        self.schedule = []
        self.min_payment = self.calculate_min_payment(months)
        self.initial_schedule = schedule_calculator.calculate(self, 0)

    def calculate_min_payment(self, months_left):
        #M = P [ I ( 1 + I )^N ] / [ ( 1 + I )^N – 1 ]
        r = Decimal(self.interest / 12)
        interest_exp = pow((1 + r), months_left)
        ann = (r * interest_exp) / (interest_exp - 1)
        monthly_payment = Decimal(self.outstanding[-1] * ann)
        return monthly_payment

    def set_min_payment(self, months_left):
        min_payment = self.calculate_min_payment(months_left)
        to_update = self.regular_payments[months_left:]
        for p in to_update:
            if p.reduce_type == ReduceType.NONE:
                p.payment = min_payment
        self.min_payment = min_payment
    
    def set_regular_payments(self, payments):
        self.regular_payments = payments

    def set_schedule(self, schedule):
        self.schedule = schedule

    def make_monthly_payment(self, month, date):
        (principal, interest) = self.get_current_monthly_payment(month)
        p = self.__make_payment(month, date, principal, interest, ReduceType.NONE)
        regular = self.regular_payments[month]
        paid = principal
        if regular.reduce_type != ReduceType.NONE:
            extra = regular.payment - self.min_payment
            paid += extra
            self.make_early_payment(month, date, extra, regular.reduce_type)
        return (paid, interest)

    def get_current_monthly_payment(self, month):
        return self.get_monthly_payment(month, self.outstanding[-1])

    def get_monthly_payment(self, month, outstanding):
        interest = outstanding * Decimal(self.interest / 12)
        paid = self.min_payment
        principal = self.pick_principal(outstanding, paid - interest)
        return (principal, interest)
    
    def __make_payment(self, month, date, principal, interest, reduce_type):
        paid = self.pick_principal(self.outstanding[-1], principal)
        o = self.outstanding[-1] - paid
        self.outstanding.append(o)
        p = PaidEntry(paid, interest, date, o)
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
            self.set_min_payment(months_left)
            self.schedule = self.schedule_calculator.calculate(self, month_to_recalculate)
        return p
    
    def pick_principal(self, outstanding, principal):
        result = principal
        if principal > outstanding or abs(principal - outstanding) < 1:
            result = outstanding
        
        return result
