# Caveats

If you run this example, your servers will not register as "healthy" to the
load balancers. This is because the code does not install MySQL into the servers
for clarity, cost, and speed of provisioning. If you switch the virtual machine
image in either GCP or AWS examples with a MySQL image, the load balancers will
have passing health checks.