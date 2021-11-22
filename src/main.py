from mortgage import Mortgage
import jsonio
import json
from amortization import Amortization, AmortizationCalculator
from schedule_calculator import ScheduleCalculator

schedule_calculator = ScheduleCalculator()
mortgage = jsonio.read_mortgage_from_file('mortgage.json', schedule_calculator)
amortization_calc = AmortizationCalculator()
amortization = amortization_calc.calculate(mortgage)
monthsPath = 'months.txt'
with open(monthsPath, 'w') as output:
    for a in amortization:
        output.write(a.__str__() + '\n')

total_interest = 0
schedulePath = 'schedule.txt'
with open(schedulePath, 'w') as output:
    for i in range(0, len(mortgage.payments)):
        p = mortgage.payments[i]
        o = mortgage.outstanding[i]
        total = p.principal + p.interest
        total_interest += p.interest
        line = f'{p.date}  | {total:12.2f} | {p.principal:12.2f} | {p.interest:12.2f} | {p.balance:12.2f} | {o:12.2f} | {total_interest:12.2f}' + '\n'
        output.write(line)

initial_interest = sum([x.interest for x in mortgage.initial_schedule])
saved = initial_interest - total_interest
print(f'You have saved {saved:.2f} with early repayments. Total interest is {total_interest:.2f}')
#jsonio.write_mortgage_to_file('mortgage_output.json', mortgage)
