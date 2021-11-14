from payment import Payment
from dateutil.relativedelta import relativedelta

class ScheduleCalculator(object):
    def calculate(self, mortgage, month_start):
        outstanding = mortgage.outstanding[-1]
        schedule = mortgage.schedule[:month_start]
        for m in range(month_start, mortgage.months):
            if outstanding == 0:
                break

            (principal, interest) = mortgage.get_monthly_payment()
            if abs(outstanding - principal) < 1:
                principal = outstanding
            
            outstanding -= principal
            date = mortgage.first_payment_date + relativedelta(months=m)
            payment = Payment(principal, interest, date, outstanding)
            schedule.append(outstanding)

        return schedule
