# Inversion of Control Example

This example requires a few steps in order to fully demonstrate
inversion of control. You will need to run the steps in the `Makefile`
for it to work end-to-end.

1. Run `make setup` from this directory. This will create
   a network and a subnet for you use.

1. It will generate a file in `network/terraform.tfstate`. The state
   file includes some JSON metadata that includes the network name.

1. Run `python main.py` to generate the `main.tf.json` file. This
   should include the network's name.

1. Run `terraform apply` and enter `yes` to create the server.

1. Run `make clean` to delete the server and the network.

> If any of the the step results in an error, re-run them. Some may have
  race conditions creating and deleting resources.