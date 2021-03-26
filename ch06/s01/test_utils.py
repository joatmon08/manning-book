import json
import os
import subprocess
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

GOOGLE_SERVICE_ACCOUNT_FILE = 'gcp-key.json'


class GoogleCredentials():
    def __init__(self):
        with open(GOOGLE_SERVICE_ACCOUNT_FILE, 'w') as f:
            f.write(os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON'))
        self.service_account_file = GOOGLE_SERVICE_ACCOUNT_FILE
        self.service_account = os.environ.get('GOOGLE_SERVICE_ACCOUNT')
        self.project = os.environ.get('GOOGLE_PROJECT')
        self.datacenter = os.environ.get('GOOGLE_REGION')


def get_server(name):
    credentials = GoogleCredentials()
    ComputeEngine = get_driver(Provider.GCE)
    driver = ComputeEngine(
        credentials.service_account,
        credentials.service_account_file,
        project=credentials.project,
        datacenter=credentials.datacenter)
    return driver.ex_get_node(
        name, credentials.datacenter)


def initialize():
    process = subprocess.Popen(
        ['terraform', 'init'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    process.communicate()
    return process.returncode


def apply():
    process = subprocess.Popen(
        ['terraform', 'apply', '-auto-approve'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def destroy():
    process = subprocess.Popen(
        ['terraform', 'destroy', '-auto-approve'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    process.communicate()
    return process.returncode
