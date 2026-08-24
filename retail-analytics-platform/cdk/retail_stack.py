from aws_cdk import Stack,RemovalPolicy,aws_s3 as s3,aws_kms as kms,aws_kinesis as kinesis,aws_glue as glue
from constructs import Construct
class RetailAnalyticsStack(Stack):
    def __init__(self,scope,id,**kwargs):
        super().__init__(scope,id,**kwargs)
        key=kms.Key(self,'Key',enable_key_rotation=True)
        self.stream=kinesis.Stream(self,'SalesStream',stream_mode=kinesis.StreamMode.ON_DEMAND,
            encryption=kinesis.StreamEncryption.KMS,encryption_key=key)
        for z in ['landing','curated','audit']:
            s3.Bucket(self,z.title(),encryption=s3.BucketEncryption.KMS,encryption_key=key,
                      block_public_access=s3.BlockPublicAccess.BLOCK_ALL,enforce_ssl=True,
                      versioned=True,removal_policy=RemovalPolicy.RETAIN)
        glue.CfnDatabase(self,'Catalog',catalog_id=self.account,database_input=glue.CfnDatabase.DatabaseInputProperty(name='retail_curated'))
