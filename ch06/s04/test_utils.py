import credentials
import subprocess
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

def get_server(name):
    ComputeEngine = get_driver(Provider.GCE)
    driver = ComputeEngine(
        credentials.GOOGLE_SERVICE_ACCOUNT,
        credentials.GOOGLE_SERVICE_ACCOUNT_FILE,
        project=credentials.GOOGLE_PROJECT,
        datacenter=credentials.GOOGLE_REGION)
    return driver.ex_get_node(
        name, credentials.GOOGLE_REGION)

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
