terraform {
    required_version = ">= 1.2.6"
}

provider aws {
    shared_credentials_files = ["/Users/mattroux/.aws/credentials"]
    region = "us-east-1"
}

resource "aws_instance" "lab4-example" {
    ami = "ami-0b0dcb5067f052a63"
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.instance.id]
    user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World" > index.html
    nohup busybox httpd -f -p ${var.server_port} &
    EOF
    tags = {
        Name = "terraform-lab4"
    }
}

resource "aws_security_group" "instance" {
    name = var.security_group_name
    description = "Allow HTTP traffic"
    ingress {
        from_port = var.server_port
        to_port = var.server_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
