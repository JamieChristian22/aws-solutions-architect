# Reviewer guide and asset provenance checklist

**Project:** aws-solutions-architect · [README](README.md) · [License](LICENSE) · [CI runs](https://github.com/JamieChristian22/aws-solutions-architect/actions)

## Five-minute review

1. Read the root README for purpose, limitations, and simulated versus measured results.
2. Open the project paths below to inspect tracked deliverables; their presence alone is not proof of correctness.
3. Review GitHub Actions for actual test outcomes. Queued or failed runs are not passing tests.
4. Verify input datasets, calculation methods, and evidence before citing performance outcomes.

### Project entry points

1. [aws-solutions-architect](<aws-solutions-architect>)
2. [clickstream-analytics](<clickstream-analytics>)
3. [consulting-toolkit](<consulting-toolkit>)
4. [finops](<finops>)
5. [healthcare-data-platform](<healthcare-data-platform>)
6. [iot-sensor-analytics](<iot-sensor-analytics>)
7. [retail-analytics-platform](<retail-analytics-platform>)

## Third-party asset and dataset provenance checklist

The following are **sample tracked candidates** for source and reuse-rights checks. Their inclusion does not imply they are external, unlicensed, or unsafe.

| Tracked asset candidate | Verification status |
| --- | --- |
| `aws-solutions-architect/finops/Cost_Model.csv` | **Not independently verified** — check origin and permissions |
| `aws-solutions-architect/finops/Savings_Model.csv` | **Not independently verified** — check origin and permissions |
| `clickstream-analytics/architecture/A_flowchart_diagram_in_the_digital_image_illustrat.png` | **Not independently verified** — check origin and permissions |
| `clickstream-analytics/finops/Cost_Model.csv` | **Not independently verified** — check origin and permissions |
| `clickstream-analytics/finops/Savings_Model.csv` | **Not independently verified** — check origin and permissions |
| `consulting-toolkit/00_intake/current-state-inventory.xlsx` | **Not independently verified** — check origin and permissions |
| `consulting-toolkit/00_intake/stakeholder-map-template.xlsx` | **Not independently verified** — check origin and permissions |
| `consulting-toolkit/01_assessment/Cloud_Maturity_Scorecard.csv` | **Not independently verified** — check origin and permissions |

For each external asset, record original source URL, creator/provider, terms, allowed redistribution and commercial use, and any required notices. For original or synthetic work, note how it was produced and ensure any modeled results are plainly labeled. The MIT repository license does not automatically grant rights to externally owned content.

**Security:** Never include API keys, private/customer data, or identifying screenshots in an evidence file. Treat current-branch scanning and historical secret scanning as separate checks.

This document is **navigation and review guidance**, not a security audit pass, ownership certification, or legal clearance. See [GitHub Actions](https://github.com/JamieChristian22/aws-solutions-architect/actions) for live test results.
