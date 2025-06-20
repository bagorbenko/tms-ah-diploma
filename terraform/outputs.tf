output "cluster_name" {
  description = "Name of the GKE cluster"
  value       = google_container_cluster.primary.name
}

output "cluster_location" {
  description = "Location of the GKE cluster"
  value       = google_container_cluster.primary.location
}

output "cluster_endpoint" {
  description = "Endpoint of the GKE cluster"
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

output "cluster_ca_certificate" {
  description = "CA certificate of the GKE cluster"
  value       = google_container_cluster.primary.master_auth.0.cluster_ca_certificate
  sensitive   = true
}

output "node_pool_name" {
  description = "Name of the node pool"
  value       = google_container_node_pool.primary_nodes.name
}

output "project_id" {
  description = "Google Cloud Project ID"
  value       = var.project
}

output "cluster_cost_info" {
  description = "Cost information for the cluster"
  value = {
    machine_type = var.machine_type
    disk_size    = var.disk_size
    node_count   = var.node_count
    image_type   = "UBUNTU_CONTAINERD"
  }
} 