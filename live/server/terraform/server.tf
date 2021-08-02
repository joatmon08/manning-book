resource "aws_instance" "ingredients" {
  ami           = "ami-0117d177e96a8481c"
  instance_type = "t3.micro"
  subnet_id     = var.subnet_id
  tags = {
    Name = local.name
  }

}
