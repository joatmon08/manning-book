# Dependency Inversion Example

This example requires a few steps in order to fully demonstrate
dependency inversion.

1. Get a GCP service account
   [key file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
   in JSON format.

1. Save that in this directory as `gcp-key.json`

1. Copy `credentials.example.py` to `credentials.py`.
   ```shell
   cp credentials.example.py credentials.py
   ```

1. Update the fields to reflect your GCP project and service account name.

1. Run the Python script. This generates a file called `main.tf.json`.
   ```shell
   python main.py
   ```

1. Initialize Terraform.
   ```shell
   terraform init
   ```

1. Apply Terraform. Enter "yes" at the prompt.
   ```shell
   terraform apply
   ```

1. Destroy resources with Terraform.
   ```shell
   terraform destroy
   ```
