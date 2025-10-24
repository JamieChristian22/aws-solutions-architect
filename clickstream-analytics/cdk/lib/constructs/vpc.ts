import { Construct } from "constructs";
import { aws_ec2 as ec2 } from "aws-cdk-lib";

export class ClickstreamVpc extends Construct {
  public readonly vpc: ec2.Vpc;
  constructor(scope: Construct, id: string) {
    super(scope, id);
    this.vpc = new ec2.Vpc(this, "Vpc", {
      ipAddresses: ec2.IpAddresses.cidr("10.20.0.0/16"),
      natGateways: 1,
      maxAzs: 2,
      subnetConfiguration: [
        { name: "public", subnetType: ec2.SubnetType.PUBLIC, cidrMask: 24 },
        { name: "private-app", subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, cidrMask: 24 }
      ]
    });
    this.vpc.addGatewayEndpoint("S3Endpoint", { service: ec2.GatewayVpcEndpointAwsService.S3 });
    [ec2.InterfaceVpcEndpointAwsService.KINESIS_STREAMS, ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
     ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH, ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_EVENTS,
     ec2.InterfaceVpcEndpointAwsService.STS, ec2.InterfaceVpcEndpointAwsService.KINESIS_FIREHOSE
    ].forEach((svc, i) => this.vpc.addInterfaceEndpoint(`Endpoint${i}`, { service: svc, subnets: { subnets: this.vpc.privateSubnets } }));
  }
}
