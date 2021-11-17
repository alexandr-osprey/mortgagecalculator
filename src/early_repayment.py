from repeat_type import RepeatType
from dateutil.relativedelta import relativedelta

class EarlyRepayment(object):
    def __init__(self, date, reduce_sum, reduce_type, repeat_type):
        self.date = date
        self.reduce_sum = reduce_sum
        self.reduce_type = reduce_type
        self.repeat_type = repeat_type

class EarlyRepaymentFiller(object):
    def fill_for_months(self, early_repayments, date_given, months):
        regular_payments = []
        first_payment_date = date_given + relativedelta(months=1)
        last_month = first_payment_date
        early_payments = self.__group_by_months(early_repayments, first_payment_date)
        payments = []
        for month in range(0, months):
            this_month_payments = []
            this_month_early = [x[1] for x in early_payments if x[0] == month]
            this_month_all = sorted(this_month_early + regular_payments, key=lambda r: r.date.day)
            for p in this_month_all:
                this_month_payments.append(EarlyRepayment(p.date, p.reduce_sum, p.reduce_type, p.repeat_type))
            s = sorted(this_month_payments, key=lambda r: r.date)
            for p in this_month_early:
                if p.repeat_type == RepeatType.REGULAR:
                    regular_payments.append(p)
            payments.append(s)
        return payments

    def __group_by_months(self, early_repayments, first_payment_date):
        months_diff = lambda date1, date2: (date1.year - date2.year) * 12 + (date1.month - date2.month)
        sorted_repayments = sorted(early_repayments, key=lambda r: r.date)
        payments_by_months = set(map(lambda r: (months_diff(r.date, first_payment_date), r), early_repayments))
        return payments_by_months
