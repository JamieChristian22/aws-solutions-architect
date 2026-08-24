from pathlib import Path
import py_compile
R=Path(__file__).resolve().parents[1]
for p in ['README.md','analytics/KPI_Catalog.md','data/Data_Quality_Rules.md','resilience/DR_Plan.md','cdk/retail_stack.py']:
    assert (R/p).exists()
py_compile.compile(str(R/'cdk/retail_stack.py'),doraise=True)
print('PASS: retail architecture')
