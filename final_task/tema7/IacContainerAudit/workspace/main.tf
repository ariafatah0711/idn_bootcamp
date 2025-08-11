resource "aws_s3_bucket" "bad_example" {
  bucket = "my-insecure-bucket"
  acl    = "public-read"
}
