provider "aws" {
  region = "eu-central-1"
}

resource "aws_vpc" "rozklad-bot-vpc" {
  cidr_block = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_hostnames = "true"
  tags = {
    Name = "ZTU-ROZKLAD-BOT-VPC"
  }
}
resource "aws_security_group" "rozklad-bot-sg" {
  name        = "ssh_access"
  description = "Allow SSH access"
  vpc_id      = aws_vpc.rozklad-bot-vpc.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "Rozklad-BOT-sg"
  }
}

resource "aws_subnet" "rozklad-bot-subnet" {
  vpc_id = aws_vpc.rozklad-bot-vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = "true"
  tags = {
    Name = "Rozklad-BOT-subnet"
  }
}

resource "aws_internet_gateway" "rozklad-bot-igw" {
  vpc_id = aws_vpc.rozklad-bot-vpc.id

  tags = {
    Name = "Rozklad-bot-igw"
  }
}
resource "aws_route_table" "AnsibleTask_route-table" {
  vpc_id = aws_vpc.rozklad-bot-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.rozklad-bot-igw.id
  }

  tags = {
    Name = "Rozklad-bot-rt"
  }
}
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.rozklad-bot-subnet.id
  route_table_id = aws_route_table.AnsibleTask_route-table.id
}
output "subnet_id" {
  value = aws_subnet.rozklad-bot-subnet.id
}
