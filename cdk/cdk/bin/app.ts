#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DataLakeStack } from '../lib/data-lake-stack';
import { ApiIngestStack } from '../lib/api-ingest-stack';
import { AnalyticsStack } from '../lib/analytics-stack';

const app = new cdk.App();

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION || 'us-east-1'
};

new DataLakeStack(app, 'RetailDataLakeStack', { env });
new ApiIngestStack(app, 'RetailApiIngestStack', { env });
new AnalyticsStack(app, 'RetailAnalyticsStack', { env });
