#!/usr/bin/env python3
import aws_cdk as cdk
from clickstream_stack import ClickstreamStack
app = cdk.App()
ClickstreamStack(app, "ClickstreamStack")
app.synth()
