#!/bin/bash

# DuckDNS Setup Script for Diploma Project
# This script helps you set up DuckDNS domains for SSL certificates

set -e

echo "🦆 DuckDNS Setup for Diploma Project"
echo "===================================="

# Check if required tools are installed
command -v curl >/dev/null 2>&1 || { echo "❌ curl is required but not installed. Aborting." >&2; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl is required but not installed. Aborting." >&2; exit 1; }

# Configuration
DUCKDNS_DOMAIN=${DUCKDNS_DOMAIN:-"diploma-project"}
DUCKDNS_TOKEN=${DUCKDNS_TOKEN:-""}
ENVIRONMENT=${ENVIRONMENT:-"prod"}

echo "📋 Configuration:"
echo "   Domain: ${DUCKDNS_DOMAIN}.duckdns.org"
echo "   Environment: ${ENVIRONMENT}"

# Check if token is provided
if [ -z "$DUCKDNS_TOKEN" ]; then
    echo ""
    echo "❓ Please provide your DuckDNS token:"
    echo "   1. Go to https://www.duckdns.org/"
    echo "   2. Sign in with your account"
    echo "   3. Copy your token from the top of the page"
    echo ""
    read -p "Enter your DuckDNS token: " DUCKDNS_TOKEN
fi

if [ -z "$DUCKDNS_TOKEN" ]; then
    echo "❌ DuckDNS token is required. Exiting."
    exit 1
fi

echo ""
echo "🔧 Setting up DuckDNS domains..."

# Function to update DuckDNS domain
update_duckdns() {
    local domain=$1
    local ip=$2
    
    echo "   Updating ${domain}.duckdns.org -> ${ip}"
    
    response=$(curl -s "https://www.duckdns.org/update?domains=${domain}&token=${DUCKDNS_TOKEN}&ip=${ip}")
    
    if [ "$response" = "OK" ]; then
        echo "   ✅ ${domain}.duckdns.org updated successfully"
    else
        echo "   ❌ Failed to update ${domain}.duckdns.org: $response"
        return 1
    fi
}

# Get external IP from LoadBalancer services
echo ""
echo "🔍 Looking for external IPs..."

API_STORE_IP=$(kubectl get svc api-store-service -n api-store-${ENVIRONMENT} -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
BOOKSHOP_IP=$(kubectl get svc bookshop-service -n bookshop-${ENVIRONMENT} -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
GRAFANA_IP=$(kubectl get svc grafana -n monitoring-${ENVIRONMENT} -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")

# Use first available IP or ask user
EXTERNAL_IP=""
if [ ! -z "$API_STORE_IP" ]; then
    EXTERNAL_IP="$API_STORE_IP"
    echo "   Found API Store IP: $API_STORE_IP"
elif [ ! -z "$BOOKSHOP_IP" ]; then
    EXTERNAL_IP="$BOOKSHOP_IP"
    echo "   Found Bookshop IP: $BOOKSHOP_IP"
elif [ ! -z "$GRAFANA_IP" ]; then
    EXTERNAL_IP="$GRAFANA_IP"
    echo "   Found Grafana IP: $GRAFANA_IP"
else
    echo "   ⚠️  No LoadBalancer IPs found in Kubernetes"
    echo ""
    echo "   You can either:"
    echo "   1. Deploy your services first to get LoadBalancer IPs"
    echo "   2. Provide an IP manually"
    echo ""
    read -p "Enter external IP address (or press Enter to skip): " MANUAL_IP
    
    if [ ! -z "$MANUAL_IP" ]; then
        EXTERNAL_IP="$MANUAL_IP"
    else
        echo "   ⏭️  Skipping IP update, will use 127.0.0.1 as placeholder"
        EXTERNAL_IP="127.0.0.1"
    fi
fi

echo "   Using IP: $EXTERNAL_IP"

# Update DuckDNS domains
echo ""
echo "🌐 Updating DuckDNS domains..."

# Main domain
update_duckdns "$DUCKDNS_DOMAIN" "$EXTERNAL_IP"

# Subdomains for services
update_duckdns "api-$DUCKDNS_DOMAIN" "$EXTERNAL_IP"
update_duckdns "bookshop-$DUCKDNS_DOMAIN" "$EXTERNAL_IP"
update_duckdns "grafana-$DUCKDNS_DOMAIN" "$EXTERNAL_IP"

# Create or update Kubernetes secret
echo ""
echo "🔐 Creating Kubernetes secret..."

kubectl create namespace kube-system --dry-run=client -o yaml | kubectl apply -f - 2>/dev/null || true

kubectl create secret generic duckdns-secret \
    --namespace kube-system \
    --from-literal=DUCKDNS_TOKEN="$DUCKDNS_TOKEN" \
    --from-literal=DUCKDNS_DOMAIN="$DUCKDNS_DOMAIN" \
    --dry-run=client -o yaml | kubectl apply -f -

echo "✅ DuckDNS secret created/updated in kube-system namespace"

# Apply DuckDNS updater
echo ""
echo "🤖 Setting up DuckDNS auto-updater..."

kubectl apply -f k8s/duckdns-updater.yaml

echo "✅ DuckDNS auto-updater deployed"

# Test domain resolution
echo ""
echo "🧪 Testing domain resolution..."

for subdomain in "" "api-" "bookshop-" "grafana-"; do
    domain="${subdomain}${DUCKDNS_DOMAIN}.duckdns.org"
    
    # Use nslookup or dig if available
    if command -v nslookup >/dev/null 2>&1; then
        resolved_ip=$(nslookup "$domain" 2>/dev/null | grep -A1 "Name:" | tail -1 | awk '{print $2}' || echo "")
    elif command -v dig >/dev/null 2>&1; then
        resolved_ip=$(dig +short "$domain" 2>/dev/null || echo "")
    else
        resolved_ip="unknown"
    fi
    
    if [ "$resolved_ip" = "$EXTERNAL_IP" ]; then
        echo "   ✅ $domain -> $resolved_ip"
    else
        echo "   ⏳ $domain -> $resolved_ip (DNS propagation may take a few minutes)"
    fi
done

# Show final information
echo ""
echo "🎉 DuckDNS Setup Complete!"
echo "========================="
echo ""
echo "Your domains:"
echo "   🌐 Main:     https://${DUCKDNS_DOMAIN}.duckdns.org"
echo "   🛒 API Store: https://api-${DUCKDNS_DOMAIN}.duckdns.org"
echo "   📚 Bookshop:  https://bookshop-${DUCKDNS_DOMAIN}.duckdns.org"
echo "   📊 Grafana:   https://grafana-${DUCKDNS_DOMAIN}.duckdns.org"
echo ""
echo "Next steps:"
echo "   1. Wait for DNS propagation (1-5 minutes)"
echo "   2. Deploy cert-manager: kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml"
echo "   3. Apply TLS certificates: kubectl apply -f k8s/tls-certificates.yaml"
echo "   4. Deploy your applications with Ingress"
echo ""
echo "🔄 The DuckDNS updater will automatically update your domains every 5 minutes"
echo ""
echo "To check the updater status:"
echo "   kubectl get cronjob duckdns-updater -n kube-system"
echo "   kubectl logs -l job-name=duckdns-updater -n kube-system" 