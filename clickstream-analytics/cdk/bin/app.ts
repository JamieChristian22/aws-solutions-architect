#!/usr/bin/env node
import 'source-map-support/register';
import { App } from 'aws-cdk-lib';
import { ClickstreamStack } from '../lib/clickstream-stack';

const app = new App();
new ClickstreamStack(app, 'ClickstreamStack', {});
