from aws_cdk import Stack,RemovalPolicy,aws_s3 as s3,aws_kms as kms,aws_iam as iam,aws_glue as glue
from constructs import Construct
class HealthcareDataPlatformStack(Stack):
    def __init__(self,scope,id,**kwargs):
        super().__init__(scope,id,**kwargs)
        key=kms.Key(self,'DataKey',enable_key_rotation=True)
        for zone in ['landing','quarantine','curated','audit']:
            s3.Bucket(self,zone.title(),encryption=s3.BucketEncryption.KMS,encryption_key=key,
                      block_public_access=s3.BlockPublicAccess.BLOCK_ALL,enforce_ssl=True,
                      versioned=True,removal_policy=RemovalPolicy.RETAIN)
        glue.CfnDatabase(self,'Catalog',catalog_id=self.account,database_input=glue.CfnDatabase.DatabaseInputProperty(name='healthcare_curated'))
