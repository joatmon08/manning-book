terraform {
  required_version = "~>0.13"
  required_providers {
    google = {
      version = "~> 3.41.0"
    }
  }
}

provider "google" {}