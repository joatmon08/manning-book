#!/usr/bin/env python
import sys
sys.path.insert(1, '../../tags/python')
import tags

from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import AwsProvider, Instance, AwsProviderDefaultTags


TEAM = 'pizza'
ENVIRONMENT = 'production'
SUFFIX = 'ingredients-python'
REGION = 'us-east-2'
SUBNET_ID = 'subnet-09c016f6c4216e06f'
AMI_ID = 'ami-0117d177e96a8481c'


class IngredientsStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        default_tags = [AwsProviderDefaultTags(
            tags=tags.get(TEAM, ENVIRONMENT))]

        AwsProvider(self, 'Aws',
                    region=REGION,
                    default_tags=default_tags
                    )

        Instance(self, 'ingredients',
                 ami=AMI_ID,
                 instance_type='t3.micro',
                 subnet_id=SUBNET_ID,
                 tags={
                     'Name': f'{TEAM}-{ENVIRONMENT}-{SUFFIX}'
                 })


app = App()
IngredientsStack(app, 'python')

app.synth()
