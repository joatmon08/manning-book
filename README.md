# Infrastructure as Code

## Prerequisites

* Sign up for a Google Cloud Platform (GCP) account and project. Check out the
  tutorial at https://console.cloud.google.com/getting-started/checklist.
* Install the gcloud command line tool. This allows you to use the terminal to
  authenticate to GCP and issue commands to GCP.
* Install Python 3 or higher.
* Install Terraform 0.13 or higher.

## Installation

Install the Python requirements.

```shell
$ pip install -r requirements.txt
```

## Run

The code listings use Python to write a Terraform JSON configuration file.
As a result, creating the resources in GCP require three steps.

1. Change to the working directory of the code listing you want to run.
   ```shell
   $ cd ch03/s01
   ```

1. Run Python.
   ```shell
   $ python main.py
   ```

1. You should have a set of files with `*.tf.json`. Then, you can
   execute Terraform to initialize and provision the resources.
   ```shell
   $ terraform init
   $ terraform apply
   ```