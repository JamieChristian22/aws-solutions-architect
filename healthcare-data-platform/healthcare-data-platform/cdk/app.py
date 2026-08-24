#!/usr/bin/env python3
import aws_cdk as cdk
from healthcare_stack import HealthcareDataPlatformStack
app=cdk.App()
HealthcareDataPlatformStack(app,'HealthcareDataPlatformStack')
app.synth()
