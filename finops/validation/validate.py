import csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]
with open(R/'1_Cost_Estimates/Service_Cost_Baseline.csv') as f:
    t=sum(float(r['MonthlyUSD']) for r in csv.DictReader(f))
assert round(t,2)==54000.0
print('PASS: FinOps baseline reconciled')
