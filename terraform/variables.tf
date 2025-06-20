variable "project" {
  type        = string
  default     = "sinuous-vent-463114-h1"
  description = "Google Cloud Project ID"
}

variable "region" {
  type        = string
  default     = "europe-west3"
  description = "Google Cloud Region"
}

variable "cluster_name" {
  type        = string
  default     = "diploma-cluster"
  description = "GKE Cluster name for diploma project"
}

variable "node_count" {
  type        = number
  default     = 1
  description = "Number of nodes in the cluster"
}

variable "machine_type" {
  type        = string
  default     = "e2-micro"
  description = "Machine type for cluster nodes"
}

variable "disk_size" {
  type        = number
  default     = 10
  description = "Disk size in GB for cluster nodes"
}