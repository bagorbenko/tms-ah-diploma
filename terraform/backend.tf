terraform {
  backend "gcs" {
    bucket = "sinuous-vent-463114-h1-terraform-state"
    prefix = "terraform/state"
  }
}