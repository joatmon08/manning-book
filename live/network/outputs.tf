output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_ids" {
  value = [aws_subnet.main.id]
}

output "region" {
  value = var.region
}