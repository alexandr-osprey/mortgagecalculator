import json
import jsonpickle
from decimal import *
from mortgage import Mortgage
from datetime import datetime
from early_repayment import EarlyRepayment, EarlyRepaymentFiller
from repeat_type import RepeatType
from reduce_type import ReduceType

def read_mortgage_from_file(path, schedule_calculator):
    with open(path, 'r') as f:
        x = json.load(f)

        ep = []
        for r in x['earlyRepayments']:
            p = EarlyRepayment(
                datetime.fromisoformat(r['date']),
                Decimal(r['sum']),
                ReduceType[r['reduceType']],
                RepeatType[r['repeatType']])
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
        return mortgage

def write_mortgage_to_file(path, mortgage):
    with open(path, 'w') as f:
        data = vars(mortgage)
        json.dump(data, f, indent=4, sort_keys=True, default=str)
        
#def write_amortization_to_file(path, amortization):

    