terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

module "tags" {
  source      = "../../tags/terraform"
  environment = var.environment
  team        = var.team
}

data "terraform_remote_state" "network" {
  backend = "local"

  config = {
    path = "../../network/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = module.tags.aws_tags
  }
}