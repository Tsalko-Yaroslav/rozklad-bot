provider "aws" {
  region = "eu-central-1"

}
module "ecr" {
  source = "./modules/ecr"
}
module "vpc" {
  source = "./modules/vpc"
}
module "ecs" {
  source = "./modules/ecs"
}