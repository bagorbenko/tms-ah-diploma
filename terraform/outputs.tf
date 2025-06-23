output "cluster_name" {
  description = "GKE cluster name"
  value       = google_container_cluster.diploma_cluster.name
}

output "cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = google_container_cluster.diploma_cluster.endpoint
  sensitive   = true
}

output "cluster_location" {
  description = "GKE cluster location"
  value       = google_container_cluster.diploma_cluster.location
}

output "cluster_ca_certificate" {
  description = "GKE cluster CA certificate"
  value       = google_container_cluster.diploma_cluster.master_auth.0.cluster_ca_certificate
  sensitive   = true
}

output "vpc_network" {
  description = "VPC network name"
  value       = google_compute_network.vpc.name
}

output "vpc_subnet" {
  description = "VPC subnet name"
  value       = google_compute_subnetwork.subnet.name
}

output "subnet_cidr" {
  description = "Subnet CIDR range"
  value       = google_compute_subnetwork.subnet.ip_cidr_range
}

output "static_bucket_name" {
  description = "Static content bucket name"
  value       = google_storage_bucket.static_content.name
}

output "static_bucket_url" {
  description = "Static content bucket URL"
  value       = "https://storage.googleapis.com/${google_storage_bucket.static_content.name}/index.html"
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}

output "project_id" {
  description = "GCP Project ID"
  value       = var.project
}

output "region" {
  description = "GCP Region"
  value       = var.region
}

output "node_pool_name" {
  description = "Primary node pool name"
  value       = google_container_node_pool.primary_nodes.name
}

output "service_account_email" {
  description = "GKE service account email (using default)"
  value       = "default"
}

output "dns_zone_name_servers" {
  description = "DNS zone name servers (production only)"
  value       = var.environment == "prod" ? google_dns_managed_zone.diploma_zone[0].name_servers : []
}

output "kubernetes_config_commands" {
  description = "Commands to configure kubectl"
  value = [
    "gcloud container clusters get-credentials ${google_container_cluster.diploma_cluster.name} --region ${var.region} --project ${var.project}",
    "kubectl create namespace api-store-${var.environment} --dry-run=client -o yaml | kubectl apply -f -",
    "kubectl create namespace bookshop-${var.environment} --dry-run=client -o yaml | kubectl apply -f -",
    "kubectl create namespace monitoring-${var.environment} --dry-run=client -o yaml | kubectl apply -f -"
  ]
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