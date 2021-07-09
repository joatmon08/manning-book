import json
import os
import subprocess


def initialize():
    print("Running terraform init...")
    process = subprocess.Popen(
        'terraform init -no-color',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def apply():
    print("Running terraform apply...")
    process = subprocess.Popen(
        'terraform apply -no-color -auto-approve',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def destroy():
    print("Running terraform destroy...")
    process = subprocess.Popen(
        'terraform destroy -no-color -auto-approve',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    process.communicate()
    return process.returncode


def status(applied):
    status = None
    for index, line in enumerate(applied):
        if "Apply complete!" in line:
            status = applied[index]
    return status


def output(name):
    print("Running terraform output...")
    process = subprocess.Popen(
        f'terraform output {name}',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr
