module "vpc" {
  source = "../vpc"
}
provider "aws" {
  region = "eu-central-1"
}
resource "aws_ecs_cluster" "rozklad-bot-cluster" {
  name = "rozklad-bot-cluster"
}
resource "aws_ecs_task_definition" "rozklad-bot-task-definition" {
  family                   = "rozklad-bot-family"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"


  container_definitions = jsonencode([
    {
      name      = "rozklad-bot-container"
      image     = "placeholder:latest"
      cpu       = 256
      memory    = 512
    }

  ])
}

resource "aws_ecs_service" "rozklad-bot-service" {
  name            = "rozklad-bot-service"
  cluster         = aws_ecs_cluster.rozklad-bot-cluster.id
  task_definition = aws_ecs_task_definition.rozklad-bot-task-definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets         = [module.vpc.subnet_id]
    security_groups = [module.vpc.sg_id]
    assign_public_ip = true
  }
}