import json
import aws
import gcp


if __name__ == "__main__":
    gcp_network = gcp.Network(name='hello-world', ip_range='10.2.0.0/16')
    aws_network = aws.Network(
        name='hello-world', ip_range='10.0.0.0/16', subnet_ip_range='10.0.1.0/24',
        peer=gcp_network.outputs())

    with open('aws-network.tf.json', 'w') as outfile:
        json.dump(aws_network.resources, outfile, sort_keys=True, indent=4)
    with open('gcp-network.tf.json', 'w') as outfile:
        json.dump(gcp_network.resources, outfile, sort_keys=True, indent=4)
