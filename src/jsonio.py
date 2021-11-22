import json
import jsonpickle
from decimal import *
from mortgage import Mortgage
from datetime import datetime
from early_repayment import EarlyRepayment, EarlyRepaymentFiller
from repeat_type import RepeatType
from reduce_type import ReduceType
from regular_payment import Payment, PaymentCalculator
from dateutil.relativedelta import relativedelta

def read_mortgage_from_file(path, schedule_calculator):
    with open(path, 'r') as f:
        x = json.load(f)

        ep = []
        for r in x['earlyRepayments']:
            startDate = datetime.fromisoformat(r['date']).date()
            endDate = getEndDate(r,startDate)
            p = EarlyRepayment(
                datetime.fromisoformat(r['date']).date(),
                Decimal(r['sum']),
                ReduceType[r['reduceType']],
                RepeatType[r['repeatType']],
                datetime.fromisoformat(r['endDate']).date())
            ep.append(p)
        
        date_given = datetime.fromisoformat(x['dateGiven']).date()
        months = int(x['months'])

        er_filler = EarlyRepaymentFiller()
        early_repayments_filled = er_filler.fill_for_months(ep, date_given, months)
        mortgage = Mortgage(
                schedule_calculator,
                Decimal(x['loan']),
                months,
                float(x['interest']) / 100,
                date_given,
                early_repayments_filled)
            
        rp = []
        for r in x['regularPayments']:
            startDate = datetime.fromisoformat(r['startDate']).date()
            endDate = getEndDate(r, startDate)
            p = Payment(
                Decimal(r['sum']),
                ReduceType[r['reduceType']],
                datetime.fromisoformat(r['startDate']).date(),
                endDate)
            rp.append(p)
        
        rp_filler = PaymentCalculator()
        default_payment = mortgage.calculate_min_payment(months)
        filled_rp = rp_filler.fill_for_months(default_payment, rp, date_given, months)
        mortgage.set_regular_payments(filled_rp)
        schedule = schedule_calculator.calculate(mortgage, 0)
        mortgage.set_schedule(schedule)
        return mortgage

def getEndDate(element, startDate):
    if 'endDate' in element.keys():
        endDate = datetime.fromisoformat(element['endDate']).date()
    else:
        endDate = startDate + relativedelta(years=50)
    return endDate

def write_mortgage_to_file(path, mortgage):
    with open(path, 'w') as f:
        data = vars(mortgage)
        json.dump(data, f, indent=4, sort_keys=True, default=str)
        
#def write_amortization_to_file(path, amortization):

    