resource "google_container_cluster" "diploma_cluster" {
  name     = "${var.cluster_name}-${var.environment}"
  location = var.region
  project  = var.project

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  # Use default network to reduce complexity and resource usage
  network    = "default"
  subnetwork = "default"

  # Disable advanced features to reduce resource requirements
  # network_policy {
  #   enabled = false
  # }

  # Disable workload identity for free tier
  # workload_identity_config {
  #   workload_pool = "${var.project}.svc.id.goog"
  # }

  # Minimal monitoring and logging for free tier
  logging_service    = "none"
  monitoring_service = "none"

  # Resource labels
  resource_labels = {
    environment = var.environment
    project     = "diploma"
    managed_by  = "terraform"
  }

  # Remove dependency on custom VPC
  # depends_on = [
  #   google_compute_network.vpc,
  #   google_compute_subnetwork.subnet,
  # ]
}

# VPC Network (commented out for free tier - using default)
# resource "google_compute_network" "vpc" {
#   name                    = "diploma-vpc-${var.environment}"
#   auto_create_subnetworks = false
#   project                 = var.project
# }

# Subnet (commented out for free tier - using default)
# resource "google_compute_subnetwork" "subnet" {
#   name          = "diploma-subnet-${var.environment}"
#   ip_cidr_range = var.environment == "prod" ? "10.0.0.0/16" : "10.${var.environment == "qa" ? 1 : 2}.0.0/16"
#   region        = var.region
#   network       = google_compute_network.vpc.name
#   project       = var.project
#
#   secondary_ip_range {
#     range_name    = "pods"
#     ip_cidr_range = var.environment == "prod" ? "172.16.0.0/14" : "172.${var.environment == "qa" ? 20 : 24}.0.0/14"
#   }
#
#   secondary_ip_range {
#     range_name    = "services"
#     ip_cidr_range = var.environment == "prod" ? "192.168.0.0/16" : "192.168.${var.environment == "qa" ? 1 : 2}.0/24"
#   }
# }

# Node pool with different configurations per environment
resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.cluster_name}-nodes-${var.environment}"
  location   = var.region
  cluster    = google_container_cluster.diploma_cluster.name
  project    = var.project

  # Node count based on environment
  node_count = var.environment == "prod" ? 2 : 1

  # Autoscaling for production
  dynamic "autoscaling" {
    for_each = var.environment == "prod" ? [1] : []
    content {
      min_node_count = var.min_node_count
      max_node_count = var.max_node_count
    }
  }

  node_config {
    preemptible  = var.environment != "prod"
    machine_type = var.environment == "prod" ? "e2-medium" : var.machine_type
    disk_size_gb = var.disk_size
    disk_type    = "pd-standard"
    image_type   = "COS_CONTAINERD"

    # Use default service account for free tier
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    # Workload Identity disabled for free tier
    # workload_metadata_config {
    #   mode = "GKE_METADATA"
    # }

    # Resource labels
    labels = {
      environment = var.environment
      node_pool   = "primary"
    }

    # Node taints for production
    dynamic "taint" {
      for_each = var.environment == "prod" ? [
        {
          key    = "environment"
          value  = "production"
          effect = "NO_SCHEDULE"
        }
      ] : []
      content {
        key    = taint.value.key
        value  = taint.value.value
        effect = taint.value.effect
      }
    }

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }

  # Management settings
  management {
    auto_repair  = true
    auto_upgrade = true  # Required for REGULAR release channel
  }

  # Upgrade settings for production
  dynamic "upgrade_settings" {
    for_each = var.environment == "prod" ? [1] : []
    content {
      max_surge       = 1
      max_unavailable = 0
    }
  }

  depends_on = [
    google_container_cluster.diploma_cluster,
  ]

  # Lifecycle management to handle updates properly
  lifecycle {
    create_before_destroy = true
    ignore_changes = [
      node_config[0].taint,
    ]
  }
}

# Service Account for GKE nodes (commented out for free tier)
# resource "google_service_account" "gke_service_account" {
#   account_id   = "gke-service-account-${var.environment}"
#   display_name = "GKE Service Account for ${var.environment}"
#   project      = var.project
# }

# IAM roles for the service account (commented out for free tier)
# resource "google_project_iam_member" "gke_service_account_roles" {
#   for_each = toset([
#     "roles/logging.logWriter",
#     "roles/monitoring.metricWriter",
#     "roles/monitoring.viewer",
#     "roles/stackdriver.resourceMetadata.writer",
#     "roles/storage.objectViewer",
#   ])
#
#   project = var.project
#   role    = each.key
#   member  = "serviceAccount:${google_service_account.gke_service_account.email}"
# }

# Cloud Storage bucket for static content
resource "google_storage_bucket" "static_content" {
  name          = "diploma-static-${var.environment}-${random_id.bucket_suffix.hex}"
  location      = "EUROPE-WEST1"
  project       = var.project
  force_destroy = var.environment != "prod"

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  # CORS settings for web access
  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  # Lifecycle rules for non-production environments
  dynamic "lifecycle_rule" {
    for_each = var.environment != "prod" ? [1] : []
    content {
      condition {
        age = 30
      }
      action {
        type = "Delete"
      }
    }
  }

  labels = {
    environment = var.environment
    project     = "diploma"
  }
}

# Random ID for bucket naming
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Make bucket public for static hosting
resource "google_storage_bucket_iam_member" "static_content_public" {
  bucket = google_storage_bucket.static_content.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# Firewall rules
resource "google_compute_firewall" "allow_http" {
  name    = "allow-http-${var.environment}"
  network = "default"
  project = var.project

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8080", "3000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"]
}

# Cloud DNS zone (for production)
resource "google_dns_managed_zone" "diploma_zone" {
  count       = var.environment == "prod" ? 1 : 0
  name        = "diploma-zone"
  dns_name    = "diploma-project.com."
  description = "DNS zone for diploma project"
  project     = var.project

  labels = {
    environment = var.environment
  }
}