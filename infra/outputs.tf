output "storage_bucket_name" {
  description = "Name of the application Cloud Storage bucket"
  value       = google_storage_bucket.app_bucket.name
}

output "service_account_email" {
  description = "Email of the application service account"
  value       = google_service_account.app_service_account.email
}

output "service_account_id" {
  description = "ID of the application service account"
  value       = google_service_account.app_service_account.id
}
