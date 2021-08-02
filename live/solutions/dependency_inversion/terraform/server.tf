data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

data "aws_subnet" "selected" {
  filter {
    name   = "tag:Team"
    values = [var.team]
  }

  filter {
    name   = "tag:Environment"
    values = [var.environment]
  }
}

resource "aws_instance" "ingredients" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = data.aws_subnet.selected.id
  tags = {
    Name = local.name
  }

}
