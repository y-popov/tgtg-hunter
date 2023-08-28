variable "PROJECT" {
  type        = string
  nullable    = false
  description = "google cloud project name"
}

terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
  backend "gcs" {
    prefix  = "tgtg"
  }
}

provider "google" {
  project = var.PROJECT
  region  = "europe-west2"
}

data "google_cloudfunctions_function" "tgtg" {
  name = "tgtg"
}

resource "google_cloud_scheduler_job" "timer" {
  name             = "tgtg-invoker"
  description      = "Triggers tgtg every 30 mins during daytime"
  schedule         = "*/30 9-22 * * *"
  attempt_deadline = format("%ds", data.google_cloudfunctions_function.tgtg.timeout)

  retry_config {
    retry_count = 3
  }

  http_target {
    http_method = "GET"
    uri         = data.google_cloudfunctions_function.tgtg.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.function_invoker.email
    }
  }
}

resource "google_service_account" "function_invoker" {
  account_id   = "function-invoker"
  display_name = "Function Invoker"
  description  = "Service account to invoke functions"
}

resource "google_project_iam_binding" "function_invoker_role" {
  project = var.PROJECT
  role    = "roles/cloudfunctions.invoker"

  members = [
    format("serviceAccount:%s", google_service_account.function_invoker.email),
  ]
}
