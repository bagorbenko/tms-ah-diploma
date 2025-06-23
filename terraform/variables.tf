variable "project" {
  type        = string
  default     = "sinuous-vent-463114-h1"
  description = "Google Cloud Project ID"
}

variable "region" {
  type        = string
  default     = "europe-west1"
  description = "Google Cloud Region"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment name (dev, qa, prod)"
  validation {
    condition     = contains(["dev", "qa", "prod"], var.environment)
    error_message = "Environment must be one of: dev, qa, prod"
  }
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

variable "min_node_count" {
  type        = number
  default     = 1
  description = "Minimum number of nodes in autoscaling group"
}

variable "max_node_count" {
  type        = number
  default     = 2
  description = "Maximum number of nodes in autoscaling group"
}

variable "enable_monitoring" {
  type        = bool
  default     = true
  description = "Enable GKE monitoring and logging"
}

variable "enable_network_policy" {
  type        = bool
  default     = true
  description = "Enable Kubernetes network policy"
}

variable "authorized_networks" {
  type = list(object({
    cidr_block   = string
    display_name = string
  }))
  default = [
    {
      cidr_block   = "0.0.0.0/0"
      display_name = "All"
    }
  ]
  description = "List of master authorized networks"
}

# DuckDNS Configuration
variable "duckdns_domain" {
  type        = string
  default     = "diploma-project"
  description = "DuckDNS subdomain name (without .duckdns.org)"
}

variable "duckdns_token" {
  type        = string
  default     = ""
  description = "DuckDNS API token for DNS updates"
  sensitive   = true
}

variable "enable_ssl" {
  type        = bool
  default     = true
  description = "Enable SSL certificates with Let's Encrypt"
}

variable "admin_email" {
  type        = string
  default     = "admin@example.com"
  description = "Admin email for Let's Encrypt certificates"
}