from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "deliverables/Solution_Design_Document.md",
    "deliverables/Operations_Runbook.md",
    "security/Threat_Model.md",
    "resilience/Disaster_Recovery_Plan.md",
    "observability/Alarm_Catalog.md",
    "finops/Cost_Model.csv",
    "finops/Savings_Model.csv",
    "iac/terraform/main.tf",
    "iac/terraform/database.tf",
    "cicd/github-actions.yml",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit(f"Missing required files: {missing}")

terraform_text = "\n".join(
    p.read_text(encoding="utf-8")
    for p in (ROOT / "iac/terraform").glob("*.tf")
)
assert "publicly_accessible         = false" in terraform_text
assert "multi_az                    = true" in terraform_text
assert "enable_key_rotation     = true" in terraform_text
assert "block_public_policy     = true" in terraform_text
assert "desired_count   = 2" in terraform_text

def sum_csv(path, column):
    with open(path, newline="", encoding="utf-8") as f:
        return sum(float(row[column]) for row in csv.DictReader(f))

baseline = sum_csv(ROOT / "finops/Cost_Model.csv", "ModeledMonthlyUSD")
savings = sum_csv(ROOT / "finops/Savings_Model.csv", "EstimatedMonthlySavingsUSD")
assert baseline > savings > 0

# Scan portfolio content, excluding this validator because it contains the scan terms by design.
scan_terms = ["todo" + ":", "tb" + "d", "insert " + "here", "lorem " + "ipsum", "<place" + "holder>"]
for p in ROOT.rglob("*"):
    if p == Path(__file__).resolve():
        continue
    if p.is_file() and p.suffix.lower() in {".md", ".tf", ".yml", ".yaml", ".py", ".csv"}:
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        hits = [term for term in scan_terms if term in text]
        if hits:
            raise AssertionError(f"Unfinished marker {hits} in {p.relative_to(ROOT)}")

print(f"PASS: {len(required)} required artifacts present")
print("PASS: key security/reliability Terraform assertions")
print(
    f"PASS: FinOps model baseline=${baseline:,.0f}, "
    f"savings=${savings:,.0f}, optimized=${baseline-savings:,.0f}"
)
print("PASS: no unfinished-content markers")
