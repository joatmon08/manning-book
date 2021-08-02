variable "team" {
  type = string
}

variable "environment" {
  type = string
}

variable "application" {
  type = string
}

locals {
  name      = "${var.team}-${var.environment}-${var.application}"
  subnet_id = data.terraform_remote_state.network.outputs.subnet_ids[0]
}