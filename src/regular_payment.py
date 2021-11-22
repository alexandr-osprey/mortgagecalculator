from reduce_type import ReduceType
from dateutil.relativedelta import relativedelta
from decimal import *

class Payment:
    def __init__(self, payment, reduce_type, start_date, end_date):
        self.payment = payment
        self.reduce_type = reduce_type
        self.start_date = start_date
        self.end_date = end_date

class PaymentCalculator:
    def fill_for_months(self, min_payment, regular_payments, date_given, months):
        result = []
        first_payment_date = date_given + relativedelta(months=1)
        for m in range(months):
            date = first_payment_date + relativedelta(months=m)
            this_month_payment = [r for r in regular_payments if r.start_date == date]
            if (len(this_month_payment) > 0):
                p = this_month_payment[-1]
                if min_payment > p.payment:
                    raise Exception("Regular payment is too small")
                to_add = p
            elif len(result) > 0 and result[-1].end_date > date:
                last = result[-1]
                to_add = Payment(last.payment, last.reduce_type, last.start_date, last.end_date)
            else:
                to_add = Payment(min_payment, ReduceType.NONE, first_payment_date, date)
            
            result.append(to_add)
        return result
