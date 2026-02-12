resource "aws_instance" "todo_app" {
  ami           = "ami-03446a3af42c5e74e"
  instance_type = "t3.micro"

  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              dnf install -y docker
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user
              EOF

  tags = {
    Name = "Todo-app-server"
  }
}
