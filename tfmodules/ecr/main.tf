provider "aws" {
  region = "eu-central-1"
}
resource "aws_ecr_repository" "rozklad-bot-ecr" {
  name = "rozklad-bot-ecr"
}