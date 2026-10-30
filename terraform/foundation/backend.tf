terraform {
  backend "s3" {
    bucket       = "openai-tfstate"
    key          = "foundation/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
