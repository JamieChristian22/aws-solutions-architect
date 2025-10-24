import { Construct } from "constructs";
import { aws_ec2 as ec2, aws_opensearchservice as os, aws_secretsmanager as sm, RemovalPolicy } from "aws-cdk-lib";

export class ClickstreamOpenSearch extends Construct {
  public readonly domain: os.Domain;
  public readonly masterSecret: sm.Secret;
  constructor(scope: Construct, id: string, vpc: ec2.Vpc) {
    super(scope, id);
    const sg = new ec2.SecurityGroup(this, "OSSG", { vpc, allowAllOutbound: true });
    vpc.privateSubnets.forEach(s => sg.addIngressRule(ec2.Peer.ipv4(s.ipv4CidrBlock), ec2.Port.tcp(443)));
    this.masterSecret = new sm.Secret(this, "OSMasterSecret", { generateSecretString: { secretStringTemplate: '{"username":"master-user"}', generateStringKey: "password" } });
    this.domain = new os.Domain(this, "OS", {
      version: os.EngineVersion.OPENSEARCH_2_13,
      vpc, vpcSubnets: [{ subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }], securityGroups: [sg],
      capacity: { dataNodes: 2, dataNodeInstanceType: "t3.small.search" },
      ebs: { volumeSize: 20 }, nodeToNodeEncryption: true, encryptionAtRest: { enabled: true }, enforceHttps: true,
      fineGrainedAccessControl: { masterUserName: "master-user", masterUserPassword: this.masterSecret.secretValueFromJson("password") },
      removalPolicy: RemovalPolicy.DESTROY
    });
  }
}
