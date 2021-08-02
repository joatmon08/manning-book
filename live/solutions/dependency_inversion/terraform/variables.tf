variable "team" {
  type = string
}

variable "environment" {
  type = string
}

variable "application" {
  type = string
}

variable "region" {
  type = string
}

locals {
  name = "${var.team}-${var.environment}-${var.application}"
}