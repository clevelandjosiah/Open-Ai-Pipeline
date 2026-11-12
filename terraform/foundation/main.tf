resource "random_id" "suffix" {
  byte_length = 4
}
resource "aws_s3_bucket" "lab" {
  # checkov:skip=CKV_AWS_145:Default SSE-S3 encryption is enough for a lab bucket; KMS adds key cost
  # checkov:skip=CKV_AWS_18:Access logging needs a second log bucket, out of scope for this lab
  # checkov:skip=CKV2_AWS_61:Lab bucket holds no data, so no lifecycle rules are needed
  # checkov:skip=CKV2_AWS_62:No downstream consumers for event notifications
  # checkov:skip=CKV_AWS_144:Cross-region replication is out of scope for a single-region lab
  bucket = "${var.prefix}-${var.environment}-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_versioning" "lab" {
  bucket = aws_s3_bucket.lab.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "lab" {
  bucket                  = aws_s3_bucket.lab.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
