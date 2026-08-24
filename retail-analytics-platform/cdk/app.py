#!/usr/bin/env python3
import aws_cdk as cdk
from retail_stack import RetailAnalyticsStack
app=cdk.App()
RetailAnalyticsStack(app,'RetailAnalyticsStack')
app.synth()
