from pathlib import Path
R=Path(__file__).resolve().parents[1]
required=['README.md','00_intake/Client_Intake_Questionnaire.md','01_assessment/Well_Architected_Assessment.md','02_design/High_Level_Design.md','03_delivery/RAID_Log.csv','04_finops/FinOps_Playbook.md','05_handover/Operations_Runbook.md','06_presales/Statement_of_Work.md','07_example_engagement/Executive_Summary.md']
missing=[x for x in required if not (R/x).exists()]
assert not missing,missing
print('PASS: consulting toolkit core artifacts')
