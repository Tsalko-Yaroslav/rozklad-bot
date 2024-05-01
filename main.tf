
provider "aws" {
  region = "eu-central-1"

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