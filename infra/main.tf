terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "google" {
  credentials = file("${path.module}/key.json")
  project     = "sinuous-vent-463114-h1"
  region      = "europe-west3"
  zone        = "europe-west3-b"
}

# Перед запуском Terraform вручную включите в GCP Console:
#   1. Service Usage API (serviceusage.googleapis.com)
#   2. Cloud Resource Manager API (cloudresourcemanager.googleapis.com)
#   3. Artifact Registry API (artifactregistry.googleapis.com)

# Общие firewall правила для HTTP/HTTPS
resource "google_compute_firewall" "http_fw" {
  name    = "allow-http-https"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
}

# Firewall для Jenkins (порт 8080)
resource "google_compute_firewall" "jenkins_fw" {
  name         = "jenkins-firewall"
  network      = "default"
  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["jenkins"]
}

# Jenkins сервер
resource "google_compute_instance" "jenkins" {
  name         = "jenkins-server"
  machine_type = "e2-medium"

  boot_disk {
    initialize_params { image = "ubuntu-os-cloud/ubuntu-2204-lts" }
  }

  network_interface {
    network       = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    # Устанавливаем необходимые пакеты
    apt-get install -y openjdk-11-jre git docker.io nginx certbot python3-certbot-nginx
    systemctl start docker
    # Настраиваем и запускаем nginx
    systemctl enable nginx
    systemctl start nginx
    # Установка и запуск Jenkins
    wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add -
    sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
    apt-get update
    apt-get install -y jenkins
    systemctl enable jenkins
    systemctl start jenkins
  EOF

  tags = ["jenkins"]
}

# Artifact Registry для Docker-образов
resource "google_artifact_registry_repository" "docker_repo" {
  project       = "sinuous-vent-463114-h1"
  location      = "europe-west3"
  repository_id = "diploma-docker-repo"
  format        = "DOCKER"
}

# Buckets для статического контента
resource "google_storage_bucket" "static_dev" {
  name          = "static-dev-mydiploma"
  location      = "EU"
  force_destroy = true
}
resource "google_storage_bucket" "static_qa" {
  name          = "static-qa-mydiploma"
  location      = "EU"
  force_destroy = true
}
resource "google_storage_bucket" "static_prod" {
  name          = "static-prod-mydiploma"
  location      = "EU"
  force_destroy = true
}

# Firewall для мониторинга (Prometheus 9090, Grafana 3000)
resource "google_compute_firewall" "monitoring_fw" {
  name         = "monitoring-firewall"
  network      = "default"
  allow {
    protocol = "tcp"
    ports    = ["9090", "3000"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["monitoring"]
}

# Сервера мониторинга: Prometheus + Grafana
resource "google_compute_instance" "monitoring" {
  name         = "monitoring-server"
  machine_type = "e2-medium"

  boot_disk {
    initialize_params { image = "ubuntu-os-cloud/ubuntu-2204-lts" }
  }

  network_interface {
    network       = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io nginx
    systemctl enable nginx
    systemctl start nginx
    # Запуск Prometheus
    docker run -d --name prometheus -p 9090:9090 prom/prometheus
    # Запуск Grafana
    docker run -d --name grafana -p 3000:3000 grafana/grafana
  EOF

  tags = ["monitoring"]
}
