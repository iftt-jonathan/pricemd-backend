terraform {
  backend "s3" {
    bucket = "428-pricemd"
    key    = "terraform/state"
    region = "us-east-2"
  }
}
