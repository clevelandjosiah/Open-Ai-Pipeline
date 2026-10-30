resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "lab" {
  bucket = "${var.prefix}-${var.environment}-${random_id.suffix.hex}"
}

# INTENTIONAL VULNERABILITY 
resource "aws_s3_bucket_public_access_block" "lab" {
  bucket                  = aws_s3_bucket.lab.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}