import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
schema=json.loads((ROOT/"schemas/clickstream_event.schema.json").read_text())
validator=Draft202012Validator(schema, format_checker=FormatChecker())

count=0
for line in (ROOT/"schemas/sample_events.jsonl").read_text().splitlines():
    event=json.loads(line)
    errors=list(validator.iter_errors(event))
    assert not errors, errors
    count+=1
print(f"PASS: {count} sample events conform to schema")
