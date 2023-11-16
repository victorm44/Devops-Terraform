provider "aws" {
  region = "us-east-1"
  version = "~> 3.0"
}

#variable "vpc_id" {
#  type    = string
#  default = "vpc-0008e62433f10f169"
#}

resource "aws_db_instance" "dbmovies" {
  identifier           = "dbmovies"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0.33"
  instance_class       = "db.t2.micro"
  name                 = "movies1"
  username             = "peliculas"
  password             = "devops123"
  publicly_accessible = true
}
