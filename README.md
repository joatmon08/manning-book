# Code Examples for Infrastructure as Code, Patterns & Practices

This repository includes code examples for
[*Infrastructure as Code, Patterns and Practices*](https://www.manning.com/books/patterns-and-practices-for-infrastructure-as-code).

> Note: For clarity and cost, some of the examples have been abbreviated.
  As a result, not all infrastructure resources will register as healthy or error
  free. Certain sections have READMEs to provide additional information
  if the code deviates from the installation and run instructions here.

## Prerequisites

- Sign up for a Google Cloud Platform (GCP) account and project. Check out the
  tutorial at https://console.cloud.google.com/getting-started/checklist.
- Install the [gcloud command line](https://cloud.google.com/sdk/docs/install) tool.
  This allows you to use the terminal to authenticate and issue commands to GCP.
- Install Python 3.9.6.
  - I use [pyenv](https://github.com/pyenv/pyenv)
    and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
    to manage my Python versions.
- Install Terraform 1.0 or higher.

## Installation

Install the Python requirements.

```shell
$ pip install -r requirements.txt
```

## Run

The code listings use Python to write a Terraform JSON configuration file.

### Google Cloud Platform (GCP)

The default code listings in the book use GCP because of its
[free tier](https://cloud.google.com/free).

1. Create a new project in GCP. Change `[PROJECT_ID]` to a unique
   project identifier of your choice. This isolates resources from
   this book from other environments or projects.
   ```shell
   $ gcloud projects create [PROJECT_ID]
   ```

1. Set the `CLOUDSDK_CORE_PROJECT` environment variable
   to the GCP project ID.
   ```shell
   $ export CLOUDSDK_CORE_PROJECT=[PROJECT_ID]
   ```

1. Authenticate to GCP.
   ```shell
   gcloud auth login
   ```

1. Change to the working directory of the code listing you want to run.
   ```shell
   $ cd ch02/s04
   ```

1. Run Python.
   ```shell
   $ python main.py
   ```

1. You should have a set of files with `*.tf.json`. Then, you can
   execute Terraform to initialize the plugin.
   ```shell
   $ terraform init
   ```

1. Apply Terraform and make sure to enter "yes" to create the resources.
   ```shell
   $ terraform apply
   ```

### Amazon Web Services (AWS)

To show some of the AWS equivalents, I also include a
few AWS examples. These will always be located in the `aws/`
directory within the chapter section.

1. [Save](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)
   your AWS access and secret key.

1. Set your environment variables for the access key.
   ```shell
   $ export AWS_ACCESS_KEY_ID=[ACCESS_KEY_ID]
   ```

1. Set your environment variables for the secret key.
   ```shell
   $ export AWS_SECRET_ACCESS_KEY=[SECRET_ACCESS_KEY]
   ```

1. Set your environment variables for the region.
   ```shell
   $ export AWS_DEFAULT_REGION=[REGION]
   ```

1. Change to the working directory of the code listing you want to run.
   ```shell
   $ cd ch02/s04/aws
   ```

1. Run Python.
   ```shell
   $ python main.py
   ```

1. You should have a set of files with `*.tf.json`. Then, you can
   execute Terraform to initialize the plugin.
   ```shell
   $ terraform init
   ```

1. Apply Terraform and make sure to enter "yes" to create the resources.
   ```shell
   $ terraform apply
   ```

### Removing Resources

You can delete resources by changing the working directory
of the code listing and destroying resources with Terraform.

```shell
$ terraform destroy
```

You can always identify the resources created by this book by examining
the labels (or tags for AWS). Most of the resources created by this
book should have a label named `purpose` set to `manning-infrastructure-as-code`,
when applicable.

## Tests

The chapter on testing uses a Python framework called
[pytest](https://docs.pytest.org/en/stable/)
to run the tests. Some of the will create resources in GCP,
as they are integration or end-to-end tests.

1. Change to the working directory of the code listing you want to run.
   ```shell
   $ cd ch05/s01
   ```

1. Run `pytest`.
   ```shell
   $ pytest .
   ```