# Hello Infrastructure as Code!

> This example qualifies for the GCP free usage tier.

## Prerequisites

* Sign up for a Google Cloud Platform (GCP) account and project. Check out the
  tutorial at https://console.cloud.google.com/getting-started/checklist.
* Install the gcloud command line tool. This allows you to use the terminal to
  authenticate to GCP and issue commands to GCP.
* Install Python 3 or higher.
* Install Terraform 0.13 or higher.

After installing the packages, you need to create a separate automation-only
account for your code to access the GCP API.

* Create a GCP service account for your code to access the GCP API. Grant the
  service account the roles/editor role in order to create resources in the
  project. For more information, check out the guide at
  https://cloud.google.com/iam/docs/creating-managing-service-accounts.
* Create and download a service account key using the instructions at
  https://cloud.google.com/iam/docs/creating-managing-service-account-keys. Save
  this JSON file! You will need it to access the GCP API.

To get started, create a directory called hello-gcp and change into the directory.

```shell
> mdkir hello-gcp
> cd hello-gcp
```

Then, copy your GCP service account key JSON file to the hello-gcp directory.

```shell
> cp ~/Downloads/<project name>-<number>.json gcp-key.json
```
