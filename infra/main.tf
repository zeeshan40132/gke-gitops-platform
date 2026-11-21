resource "google_storage_bucket" "app_bucket" {
  name          = "gitops-platform-demo-bucket"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true

  labels = {
    project     = "gitops-platform"
    environment = "local"
    managed_by  = "opentofu"
  }
}

resource "google_service_account" "app_service_account" {
  account_id   = "gitops-platform-app"
  display_name = "GitOps Platform Application"
  description  = "Service account managed by OpenTofu in the local emulator"
}

resource "google_storage_bucket_iam_member" "bucket_access" {
  bucket = google_storage_bucket.app_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.app_service_account.email}"
}