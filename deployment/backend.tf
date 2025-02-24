terraform {
  backend "s3" {
    bucket = "pricemd"
    key    = "terraform/state"
    region = "us-east-1"
  }
}
