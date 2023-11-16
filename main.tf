provider "aws" {
  region = "us-east-1"  # Cambia esto a tu región preferida de AWS
}

resource "aws_instance" "flask_app" {
  ami           = "ami-0c55b159cbfafe1f0"  # AMI de Amazon Linux 2
  instance_type = "t2.micro"  # Tipo de instancia
  key_name      = "tu-key-pair"  # Cambia esto a tu clave SSH existente
  security_group = ["tu-security-group"]  # Cambia esto a tu grupo de seguridad existente

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y python3
              git clone https://github.com/victorm44/Devops-Terraform.git  
              pip3 install -r requirements.txt
              python3 main.py
              EOF
}

output "public_ip" {
  value = aws_instance.flask_app.public_ip
}
