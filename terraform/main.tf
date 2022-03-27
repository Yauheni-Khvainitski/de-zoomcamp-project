terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}" 
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = false
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# # DWH
# # Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
# resource "google_bigquery_dataset" "dataset" {
#   dataset_id = var.BQ_DATASET
#   project    = var.project
#   location   = var.region
# }

# airflow VM
resource "google_compute_instance_from_machine_image" "vm" {
  provider = google-beta
  project  = var.project
  name     = "airflow-tf"
  zone     = "europe-west1-b"

  source_machine_image = "projects/${var.project}/global/machineImages/base-vm-image-2"

  metadata_startup_script = "cd de-zoomcamp-project/airflow/ && git pull && docker-compose up airflow-init && docker-compose up"
}