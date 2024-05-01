output "vpc_id" {
  value = aws_vpc.rozklad-bot-vpc.id
}
output "sg_id" {
  value = aws_security_group.rozklad-bot-sg.id
}