import { Construct } from "constructs";
import { RemovalPolicy } from "aws-cdk-lib";
import * as cognito from "aws-cdk-lib/aws-cognito";
import * as iam from "aws-cdk-lib/aws-iam";

export class ClickstreamCognito extends Construct {
  public readonly userPool: cognito.UserPool;
  public readonly userPoolClient: cognito.UserPoolClient;
  public readonly identityPool: cognito.CfnIdentityPool;
  constructor(scope: Construct, id: string) {
    super(scope, id);
    this.userPool = new cognito.UserPool(this, "UserPool", {
      selfSignUpEnabled: true, signInAliases: { email: true }, removalPolicy: RemovalPolicy.DESTROY
    });
    this.userPoolClient = this.userPool.addClient("Client", { authFlows: { userSrp: true } });
    this.identityPool = new cognito.CfnIdentityPool(this, "IdentityPool", {
      allowUnauthenticatedIdentities: False, cognitoIdentityProviders: [{ clientId: this.userPoolClient.userPoolClientId, providerName: this.userPool.userPoolProviderName }]
    } as any);
  }
}
