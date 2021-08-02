output "aws_tags" {
    value = {
        Team = var.team
        Environment = var.environment
        Automation = "terraform"
    }
}