terraform {
  backend "gcs" {
    bucket = "tms-ah-diploma-terraform-state-1750537145"
    prefix = "terraform/state"
  }
}
