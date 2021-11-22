from dateutil.relativedelta import relativedelta

class Amortization(object):
    def __init__(self, month, date, balance, paid, interest, ending_balance, total_interest):
        self.month = month
        self.date = date
        self.balance = balance
        self.paid = paid
        self.interest = interest
        self.total = self.paid + self.interest
        self.ending_balance = ending_balance
        self.total_interest = total_interest

    def __str__(self):
        return f'{self.month:5} | {self.date} | {self.paid:12.2f} | {self.interest:12.2f} | {self.total:12.2f} | {self.ending_balance:12.2f} | {self.total_interest:12.2f}'

class AmortizationCalculator:
    def calculate(self, mortgage):
        amortizations = []
        total_interest = 0
        last_month = mortgage.first_payment_date
        for month in range(0, mortgage.months):
            if mortgage.outstanding[-1] <= 0:
                break
            
            balance_before = mortgage.outstanding[-1]
            date = mortgage.first_payment_date + relativedelta(months=month)
            paid = 0
            before_comparer = lambda d: d < date
            paid += self.make_early_payments(mortgage, month, before_comparer)
            
            if mortgage.outstanding[-1] <= 0:
                break
            (principal, interest) = mortgage.make_monthly_payment(month, date)
            paid += principal
            total_interest +=  interest

            after_comparer = lambda d: d >= date
            paid += self.make_early_payments(mortgage, month, after_comparer)
            a = Amortization(month + 1, date,  balance_before, paid, interest, mortgage.outstanding[-1], total_interest)
            amortizations.append(a)
        return amortizations

    def make_early_payments(self, mortgage, month, date_comparer):
        paid = 0
        filtered_payments = [x for x in mortgage.early_repayments[month] if date_comparer(x.date)]
        for b in filtered_payments:
            if mortgage.outstanding[-1] <= 0:
                break
            mortgage.make_early_payment(month, b.date, b.reduce_sum, b.reduce_type)
            paid += b.reduce_sum
        
        return paid
