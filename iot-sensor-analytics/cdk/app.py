#!/usr/bin/env python3
import aws_cdk as cdk
from iot_stack import IotStack

app = cdk.App()
IotStack(app, "IotSensorAnalyticsStack")
app.synth()
