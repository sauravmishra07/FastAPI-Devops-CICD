#  Output of the public ip address of the instance 
output "instance_public_ip" {
  value = aws_instance.todo_app.public_ip
}

