#!/usr/bin/env python
import sys
sys.path.insert(1, '../../tags/python')
import tags

import boto3
import json
from dateutil import parser
from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import AwsProvider, Instance, AwsProviderDefaultTags


NETWORK_STATE = '../../network/terraform.tfstate'
TEAM = 'pizza'
ENVIRONMENT = 'production'
SUFFIX = 'ingredients-python'


def open_terraform_state():
    with open(NETWORK_STATE, 'r') as f:
        state = json.load(f)
    return state['outputs']


def client(region):
    return boto3.client('ec2', region_name=region)


def get_ubuntu_ami(client):
    images = client.describe_images(
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


def get_subnet_id(client):
    subnets = client.describe_subnets(
        Filters=[
            {
                'Name': 'tag:Team',
                'Values': [
                    TEAM,
                ]
            },
            {
                'Name': 'tag:Environment',
                        'Values': [
                            ENVIRONMENT,
                        ]
            },
        ]
    )
    return subnets['Subnets'][0]['SubnetId']


class IngredientsStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        region = open_terraform_state()['region']['value']
        ec2_client = client(region)
        subnet_id = get_subnet_id(ec2_client)
        default_tags = [AwsProviderDefaultTags(
            tags=tags.get(TEAM, ENVIRONMENT))]
        ami_id = get_ubuntu_ami(ec2_client)

        AwsProvider(self, 'Aws',
                    region=REGION,
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
