variable "region" {
  type = string
}

variable "team" {
  type = string
}

variable "environment" {
  type = string
}

variable "cidr_block" {
  type = string
}

locals {
  name = "${var.team}-${var.environment}"
}