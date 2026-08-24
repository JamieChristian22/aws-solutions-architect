from pathlib import Path
import py_compile
R=Path(__file__).resolve().parents[1]
for p in ['README.md','security/HIPAA_Aligned_Control_Matrix.md','data-governance/Deidentification_Rules.md','resilience/DR_Plan.md','cdk/healthcare_stack.py']:
    assert (R/p).exists()
py_compile.compile(str(R/'cdk/healthcare_stack.py'),doraise=True)
print('PASS: healthcare architecture')
