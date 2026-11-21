provider "google" {
  project = "floci-local"
  region  = "us-central1"

  storage_custom_endpoint          = "http://localhost:4588/storage/v1/"
  iam_custom_endpoint               = "http://localhost:4588/"
  resource_manager_custom_endpoint  = "http://localhost:4588/v1/"
  service_usage_custom_endpoint     = "http://localhost:4588/v1/"

  access_token = "floci-fake-token"
}