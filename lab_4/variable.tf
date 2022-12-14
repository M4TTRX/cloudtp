variable "server_port" { 
    description = "HTTP request port"
    type = number
    default = 80 
}

variable "security_group_name" {
    type = string
    default = "terraform-lab4-instance"
}