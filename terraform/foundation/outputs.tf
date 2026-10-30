output "bucket_name" {
  value = aws_s3_bucket.lab.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.lab.arn
}
