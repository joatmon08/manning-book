import subprocess


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


def output(variable_name):
    process = subprocess.Popen(
        ['terraform', 'output', '-raw', variable_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr


def destroy():
    process = subprocess.Popen(
        ['terraform', 'destroy', '-auto-approve'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    process.communicate()
    return process.returncode
