resource "google_container_cluster" "primary" {
  name               = var.cluster_name
  location           = var.region
  initial_node_count = 1

  remove_default_node_pool = true

  node_config {
    machine_type = var.machine_type
    disk_size_gb = var.disk_size
    disk_type    = "pd-standard"
    
    image_type = "UBUNTU_CONTAINERD"
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
    
    labels = {
      environment = "diploma"
      cost_center = "education"
    }
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.cluster_name}-node-pool"
  cluster    = google_container_cluster.primary.name
  location   = var.region
  node_count = var.node_count

  node_config {
    machine_type = var.machine_type
    disk_size_gb = var.disk_size
    disk_type    = "pd-standard"
    
    image_type = "UBUNTU_CONTAINERD"
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
    
    labels = {
      environment = "diploma"
      cost_center = "education"
    }
    
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 2
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}