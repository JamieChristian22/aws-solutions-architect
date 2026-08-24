#!/usr/bin/env python3
import aws_cdk as cdk
from iot_stack import IoTSensorAnalyticsStack
app=cdk.App()
IoTSensorAnalyticsStack(app,"IoTSensorAnalyticsStack")
app.synth()
