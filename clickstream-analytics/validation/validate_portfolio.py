from pathlib import Path
import csv, json, py_compile

ROOT=Path(__file__).resolve().parents[1]

required=[
"README.md","architecture/Capacity_Model.md","analytics/athena_queries.sql",
"cdk/clickstream_stack.py","lambda/ingest/handler.py","lambda/processor/handler.py",
"schemas/clickstream_event.schema.json","security/Threat_Model.md",
"resilience/Disaster_Recovery_Plan.md","finops/Cost_Model.csv","ops/Operations_Runbook.md"
]
missing=[x for x in required if not (ROOT/x).exists()]
assert not missing, missing

json.loads((ROOT/"schemas/clickstream_event.schema.json").read_text())
py_compile.compile(str(ROOT/"lambda/ingest/handler.py"), doraise=True)
py_compile.compile(str(ROOT/"lambda/processor/handler.py"), doraise=True)
py_compile.compile(str(ROOT/"cdk/app.py"), doraise=True)
py_compile.compile(str(ROOT/"cdk/clickstream_stack.py"), doraise=True)
py_compile.compile(str(ROOT/"clients/generator/send_events.py"), doraise=True)

def total(path,col):
    with open(path,newline="",encoding="utf-8") as f:
        return sum(float(x[col]) for x in csv.DictReader(f))
baseline=total(ROOT/"finops/Cost_Model.csv","ModeledMonthlyUSD")
savings=total(ROOT/"finops/Savings_Model.csv","ModeledMonthlySavingsUSD")
assert baseline>savings>0

terms=["tb"+"d","lorem "+"ipsum","<place"+"holder>","insert "+"here"]
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix.lower() in {".md",".py",".sql",".json",".yml",".yaml",".csv"}:
        if p.resolve()==Path(__file__).resolve(): continue
        txt=p.read_text(encoding="utf-8",errors="ignore").lower()
        hits=[t for t in terms if t in txt]
        assert not hits,(p,hits)

print(f"PASS: {len(required)} core artifacts")
print("PASS: Python syntax")
print("PASS: JSON schema parse")
print(f"PASS: cost model ${baseline:,.0f} baseline / ${savings:,.0f} modeled savings")
print("PASS: no unfinished-content markers")
