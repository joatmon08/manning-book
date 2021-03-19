# Dependency Inversion Example

This example uses only Terraform to demonstrate dependency inversion.

1. Run `terraform init` to initialize Terraform.

1. Run `terraform apply` and enter `yes` to create the server.

1. Run `make clean` to delete the server and the network.

> If any of the the step results in an error, re-run them. Some may have
  race conditions creating and deleting resources.