
provider "aws" {
  region = "eu-central-1"

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