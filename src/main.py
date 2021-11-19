from mortgage import Mortgage
import jsonio
import json
from amortization import Amortization, AmortizationCalculator
from schedule_calculator import ScheduleCalculator

schedule_calculator = ScheduleCalculator()
mortgage = jsonio.read_mortgage_from_file('mortgage.json', schedule_calculator)
amortization_calc = AmortizationCalculator()
amortization = amortization_calc.calculate(mortgage)
for a in amortization:
    print(a)

total_interest = 0
for i in range(0, len(mortgage.payments)):
    p = mortgage.payments[i]
    o = mortgage.outstanding[i]
    total = p.principal + p.interest
    total_interest += p.interest
    print(f'{p.date}  | {total:12.2f} | {p.principal:12.2f} | {p.interest:12.2f} | {p.balance:12.2f} | {o:12.2f} | {total_interest:12.2f}')
#jsonio.write_mortgage_to_file('mortgage_output.json', mortgage)
