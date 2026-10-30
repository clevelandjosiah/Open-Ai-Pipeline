variable "region" {
  type    = string
  default = "us-east-1"
}

variable "prefix" {
  type    = string
  default = "oaib"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "tags" {
  type = map(string)
  default = {
    Environment = "dev"
    ManagedBy   = "Terraform"
    Project     = "Open-Ai-Pipeline"
  }
}
