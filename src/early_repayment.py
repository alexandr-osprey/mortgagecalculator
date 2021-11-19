from repeat_type import RepeatType
from dateutil.relativedelta import relativedelta

class EarlyRepayment(object):
    def __init__(self, date, reduce_sum, reduce_type, repeat_type, end_date):
        self.date = date
        self.reduce_sum = reduce_sum
        self.reduce_type = reduce_type
        self.repeat_type = repeat_type
        self.end_date = end_date

class EarlyRepaymentFiller(object):
    def fill_for_months(self, early_repayments, date_given, months):
        regular_payments = []
        first_payment_date = date_given + relativedelta(months=1)
        early_payments = self.__group_by_months(early_repayments, first_payment_date)
        payments = []
        for month in range(0, months):
            date = first_payment_date + relativedelta(months=month)
            this_month_payments = []
            this_month_early = [x[1] for x in early_payments if x[0] == month]
            this_month_all = sorted(this_month_early + regular_payments, key=lambda r: r.date.day)
            for p in this_month_all:
                months_to_add = self.months_diff(date, p.date)
                corrected_date = p.date + relativedelta(months=months_to_add)
                if corrected_date < p.end_date:
                    this_month_payments.append(EarlyRepayment(corrected_date, p.reduce_sum, p.reduce_type, p.repeat_type, p.end_date))
                else:
                    regular_payments.remove(p)
            s = sorted(this_month_payments, key=lambda r: r.date)
            for p in this_month_early:
                if p.repeat_type == RepeatType.REGULAR:
                    regular_payments.append(p)
            payments.append(s)
        return payments

    def __group_by_months(self, early_repayments, first_payment_date):
        sorted_repayments = sorted(early_repayments, key=lambda r: r.date)
        payments_by_months = set(map(lambda r: (self.months_diff(r.date, first_payment_date), r), early_repayments))
        return payments_by_months

    def months_diff(self, date1, date2):
        return  (date1.year - date2.year) * 12 + (date1.month - date2.month)