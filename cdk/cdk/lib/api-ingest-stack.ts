import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as apigw from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as kinesis from 'aws-cdk-lib/aws-kinesis';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as waf from 'aws-cdk-lib/aws-wafv2';

export class ApiIngestStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const streamName = cdk.Fn.importValue('RetailDataLakeStack:ExportsOutputKinesisStreamName');
    // In a single-app context, you could instead look up via SSM or pass as props.

    const stream = kinesis.Stream.fromStreamName(this, 'EventsStream', streamName);

    const fn = new lambda.Function(this, 'IngestFn', {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('../services/ingest-api'),
      environment: { STREAM_NAME: stream.streamName }
    });

    stream.grantWrite(fn);

    const api = new apigw.RestApi(this, 'IngestApi', {
      deployOptions: { stageName: 'prod' }
    });

    const events = api.root.addResource('events');
    events.addMethod('POST', new apigw.LambdaIntegration(fn));

    // Basic WAFv2 web ACL with AWS managed rules
    const acl = new waf.CfnWebACL(this, 'ApiWaf', {
      defaultAction: { allow: {} },
      scope: 'REGIONAL',
      visibilityConfig: { cloudWatchMetricsEnabled: true, metricName: 'api-waf', sampledRequestsEnabled: true },
      name: 'RetailApiWaf',
      rules: [{
        name: 'AWSManagedCommon',
        priority: 1,
        overrideAction: { none: {} },
        statement: { managedRuleGroupStatement: { vendorName: 'AWS', name: 'AWSManagedRulesCommonRuleSet' } },
        visibilityConfig: { cloudWatchMetricsEnabled: true, metricName: 'aws-common', sampledRequestsEnabled: true }
      }]
    });

    new waf.CfnWebACLAssociation(this, 'ApiWafAssoc', {
      resourceArn: api.deploymentStage.stageArn,
      webAclArn: acl.attrArn
    });

    new cdk.CfnOutput(this, 'ApiUrl', { value: api.url });
  }
}
