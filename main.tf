variable "AWS_ACCESS_KEY_ID" {
  default = ""
}
variable "AWS_SECRET_ACCESS_KEY" {
  default = ""
}
provider "aws" {
  region = "eu-central-1"
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}
terraform {
  backend "s3" {
    bucket = "terraform-bucket-rozklad-bot"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }
}
module "ecr" {
  source = "./tfmodules/ecr"
}
module "vpc" {
  source = "./tfmodules/vpc"
}
module "ecs" {
  source = "./tfmodules/ecs"
}