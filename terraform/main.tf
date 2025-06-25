resource "google_container_cluster" "diploma_cluster" {
  name     = "${var.cluster_name}-${var.environment}"
  location = var.region
  project  = var.project

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = "default"
  subnetwork = "default"



  logging_service    = "none"
  monitoring_service = "none"

  resource_labels = {
    environment = var.environment
    project     = "diploma"
    managed_by  = "terraform"
  }

}



resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.cluster_name}-nodes-${var.environment}"
  location   = var.region
  cluster    = google_container_cluster.diploma_cluster.name
  project    = var.project

  node_count = var.environment == "prod" ? 2 : 1

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

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]


    labels = {
      environment = var.environment
      node_pool   = "primary"
    }

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

  management {
    auto_repair  = true
    auto_upgrade = true  # Required for REGULAR release channel
  }

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

  lifecycle {
    create_before_destroy = true
    ignore_changes = [
      node_config[0].taint,
    ]
  }
}



resource "google_storage_bucket" "static_content" {
  name          = "diploma-static-${var.environment}-${random_id.bucket_suffix.hex}"
  location      = "EUROPE-WEST1"
  project       = var.project
  force_destroy = var.environment != "prod"

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

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

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket_iam_member" "static_content_public" {
  bucket = google_storage_bucket.static_content.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

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