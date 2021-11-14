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
#jsonio.write_mortgage_to_file('mortgage_output.json', mortgage)
