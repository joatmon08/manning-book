variable "team" {
  type = string
}

variable "environment" {
  type = string
}

variable "application" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "region" {
  type = string
}

locals {
  name = "${var.team}-${var.environment}-${var.application}"
}