from pathlib import Path
import json,csv,py_compile
R=Path(__file__).resolve().parents[1]
req=["README.md","architecture/Capacity_Model.md","schemas/telemetry.schema.json","cdk/iot_stack.py","lambda/stream_processor/index.py","security/IoT_Security_Model.md","resilience/Disaster_Recovery_Plan.md","ops/Operations_Runbook.md","finops/Cost_Model.csv"]
assert not [x for x in req if not (R/x).exists()]
json.loads((R/"schemas/telemetry.schema.json").read_text())
for f in ["cdk/app.py","cdk/iot_stack.py","lambda/stream_processor/index.py","device-simulator/publish_telemetry.py"]:
    py_compile.compile(str(R/f),doraise=True)
def total(path,col):
    with open(path,newline="",encoding="utf-8") as f:return sum(float(r[col]) for r in csv.DictReader(f))
b=total(R/"finops/Cost_Model.csv","ModeledMonthlyUSD"); s=total(R/"finops/Savings_Model.csv","ModeledMonthlySavingsUSD"); assert b>s>0
terms=["tb"+"d","lorem "+"ipsum","<place"+"holder>","insert "+"here"]
for p in R.rglob("*"):
    if p.is_file() and p.suffix.lower() in {".md",".py",".sql",".json",".yml",".yaml",".csv"} and p.resolve()!=Path(__file__).resolve():
        txt=p.read_text(encoding="utf-8",errors="ignore").lower(); assert not [t for t in terms if t in txt]
print(f"PASS: {len(req)} core artifacts")
print("PASS: Python/CDK syntax")
print("PASS: telemetry schema JSON")
print(f"PASS: FinOps ${b:,.0f} baseline / ${s:,.0f} savings")
print("PASS: no unfinished-content markers")
