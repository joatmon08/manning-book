#!/usr/bin/env python
import sys
sys.path.insert(1, '../../tags/python')
import tags

from imports.aws import AwsProvider, Instance, AwsProviderDefaultTags
from cdktf import App, TerraformStack
from constructs import Construct
from dateutil import parser
import json
import boto3


NETWORK_STATE = '../../network/terraform.tfstate'
TEAM = 'pizza'
ENVIRONMENT = 'production'
SUFFIX = 'ingredients-python'


def get_ubuntu_ami(region):
    ec2_client = boto3.client('ec2', region_name=region)
    images = ec2_client.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': [
                    'ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*',
                ]
            },
            {
                'Name': 'virtualization-type',
                'Values': [
                    'hvm',
                ]
            },
        ],
        Owners=['099720109477']
    )
    latest = None
    image_list = images['Images']
    for image in image_list:
        if not latest:
            latest = image
            continue
        if parser.parse(image['CreationDate']) > parser.parse(latest['CreationDate']):
            latest = image
    return latest['ImageId']


def open_terraform_state():
    with open(NETWORK_STATE, 'r') as f:
        state = json.load(f)
    return state['outputs']


class IngredientsStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        region = open_terraform_state()['region']['value']
        subnet_id = open_terraform_state()['subnet_ids']['value'][0]
        default_tags = [AwsProviderDefaultTags(
            tags=tags.get(TEAM, ENVIRONMENT))]
        ami_id = get_ubuntu_ami(region)

        AwsProvider(self, 'Aws',
                    region=region,
                    default_tags=default_tags
                    )

        Instance(self, 'ingredients',
                 ami=ami_id,
                 instance_type='t3.micro',
                 subnet_id=subnet_id,
                 tags={
                     'Name': f'{TEAM}-{ENVIRONMENT}-{SUFFIX}'
                 })


app = App()
IngredientsStack(app, 'python')

app.synth()
