setup:
	cd network && terraform init && terraform apply -auto-approve

clean:
	terraform destroy -auto-approve
	cd network && terraform destroy -auto-approve