"""
Advanced cloud-native blueprint generation skills.
Enables agents to generate production-ready infrastructure as code.
"""
from typing import Dict, Any, List, Optional
import json


def generate_kubernetes_deployment(
    app_name: str,
    image: str,
    replicas: int = 3,
    port: int = 8080,
    env_vars: Optional[Dict[str, str]] = None
) -> str:
    """
    Generate Kubernetes Deployment manifest.
    
    Args:
        app_name: Application name
        image: Docker image (e.g., myapp:v1.0.0)
        replicas: Number of replicas
        port: Container port
        env_vars: Environment variables dict
        
    Returns:
        YAML manifest as string
    """
    env_vars = env_vars or {}
    env_list = [{"name": k, "value": v} for k, v in env_vars.items()]
    
    manifest = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  labels:
    app: {app_name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {image}
        ports:
        - containerPort: {port}
        env:
"""
    for env in env_list:
        manifest += f"        - name: {env['name']}\n          value: \"{env['value']}\"\n"
    
    manifest += f"""        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: {port}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: {port}
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-service
spec:
  selector:
    app: {app_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: {port}
  type: LoadBalancer
"""
    return manifest


def generate_docker_compose(
    services: List[Dict[str, Any]],
    network_name: str = "app-network"
) -> str:
    """
    Generate Docker Compose configuration.
    
    Args:
        services: List of service configurations
        network_name: Docker network name
        
    Returns:
        docker-compose.yml content
    """
    compose = f"""version: '3.8'

services:
"""
    
    for service in services:
        name = service.get('name', 'app')
        image = service.get('image', 'nginx:latest')
        ports = service.get('ports', [])
        env_vars = service.get('env', {})
        volumes = service.get('volumes', [])
        depends_on = service.get('depends_on', [])
        
        compose += f"""  {name}:
    image: {image}
    container_name: {name}
"""
        
        if ports:
            compose += "    ports:\n"
            for port_mapping in ports:
                compose += f"      - \"{port_mapping}\"\n"
        
        if env_vars:
            compose += "    environment:\n"
            for key, value in env_vars.items():
                compose += f"      {key}: {value}\n"
        
        if volumes:
            compose += "    volumes:\n"
            for volume in volumes:
                compose += f"      - {volume}\n"
        
        if depends_on:
            compose += "    depends_on:\n"
            for dep in depends_on:
                compose += f"      - {dep}\n"
        
        compose += f"    networks:\n      - {network_name}\n"
        compose += "    restart: unless-stopped\n\n"
    
    compose += f"""networks:
  {network_name}:
    driver: bridge
"""
    
    return compose


def generate_terraform_module(
    provider: str,
    resource_type: str,
    resource_name: str,
    config: Dict[str, Any]
) -> str:
    """
    Generate Terraform module.
    
    Args:
        provider: Cloud provider (aws, azure, gcp)
        resource_type: Resource type (e.g., 'vpc', 'vm', 'storage')
        resource_name: Resource identifier
        config: Resource configuration
        
    Returns:
        Terraform .tf file content
    """
    tf_content = f"""# Terraform module for {resource_type}
# Provider: {provider}

terraform {{
  required_version = ">= 1.0"
  required_providers {{
    {provider} = {{
      source  = "hashicorp/{provider}"
      version = "~> 5.0"
    }}
  }}
}}

provider "{provider}" {{
  region = var.region
}}

"""
    
    # Add variables
    tf_content += """variable "region" {
  description = "Cloud region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}

"""
    
    # Add resource
    if provider == "aws":
        if resource_type == "vpc":
            tf_content += f"""resource "aws_vpc" "{resource_name}" {{
  cidr_block           = "{config.get('cidr', '10.0.0.0/16')}"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name        = "{resource_name}"
    Environment = var.environment
  }}
}}
"""
        elif resource_type == "s3_bucket":
            tf_content += f"""resource "aws_s3_bucket" "{resource_name}" {{
  bucket = "{config.get('bucket_name', resource_name)}"

  tags = {{
    Name        = "{resource_name}"
    Environment = var.environment
  }}
}}

resource "aws_s3_bucket_versioning" "{resource_name}_versioning" {{
  bucket = aws_s3_bucket.{resource_name}.id
  
  versioning_configuration {{
    status = "Enabled"
  }}
}}

resource "aws_s3_bucket_server_side_encryption_configuration" "{resource_name}_encryption" {{
  bucket = aws_s3_bucket.{resource_name}.id

  rule {{
    apply_server_side_encryption_by_default {{
      sse_algorithm = "AES256"
    }}
  }}
}}
"""
    
    # Add outputs
    tf_content += f"""
output "{resource_name}_id" {{
  description = "ID of the {resource_type}"
  value       = {provider}_{resource_type}.{resource_name}.id
}}
"""
    
    return tf_content


def generate_github_actions_pipeline(
    app_name: str,
    build_steps: List[str],
    deploy_target: str = "kubernetes"
) -> str:
    """
    Generate GitHub Actions CI/CD pipeline.
    
    Args:
        app_name: Application name
        build_steps: List of build commands
        deploy_target: Deployment target (kubernetes, docker, aws)
        
    Returns:
        GitHub Actions workflow YAML
    """
    workflow = f"""name: CI/CD Pipeline - {app_name}

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{{{ github.repository }}}}

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{{{ env.REGISTRY }}}}
          username: ${{{{ github.actor }}}}
          password: ${{{{ secrets.GITHUB_TOKEN }}}}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{{{version}}}}
            type=semver,pattern={{{{major}}}}.{{{{minor}}}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{{{ steps.meta.outputs.tags }}}}
          labels: ${{{{ steps.meta.outputs.labels }}}}
          cache-from: type=gha
          cache-to: type=gha,mode=max

"""
    
    if deploy_target == "kubernetes":
        workflow += """  deploy:
    needs: build-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f k8s/
          kubectl rollout status deployment/{app_name}

      - name: Verify deployment
        run: |
          kubectl get pods -l app={app_name}
          kubectl get services
"""
    
    return workflow


def generate_monitoring_stack() -> str:
    """
    Generate Prometheus + Grafana monitoring stack.
    
    Returns:
        Kubernetes manifests for monitoring
    """
    manifests = """# Prometheus + Grafana Monitoring Stack

apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
---
apiVersion:v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: monitoring
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          value: admin
---
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: monitoring
spec:
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
  type: LoadBalancer
"""
    return manifests


def estimate_cloud_costs(
    resources: List[Dict[str, Any]],
    provider: str = "aws",
    region: str = "us-east-1"
) -> Dict[str, Any]:
    """
    Estimate monthly cloud costs.
    
    Args:
        resources: List of cloud resources
        provider: Cloud provider
        region: Cloud region
        
    Returns:
        Cost estimate breakdown
    """
    # Simplified cost estimation
    cost_map = {
        "aws": {
            "t3.micro": 7.30,
            "t3.small": 14.60,
            "t3.medium": 29.20,
            "s3_storage_gb": 0.023,
            "rds_t3.micro": 12.41,
        }
    }
    
    total_cost = 0
    breakdown = []
    
    for resource in resources:
        resource_type = resource.get('type')
        quantity = resource.get('quantity', 1)
        
        if provider in cost_map and resource_type in cost_map[provider]:
            unit_cost = cost_map[provider][resource_type]
            cost = unit_cost * quantity
            total_cost += cost
            
            breakdown.append({
                "resource": resource.get('name', resource_type),
                "type": resource_type,
                "quantity": quantity,
                "unit_cost": unit_cost,
                "total_cost": cost
            })
    
    return {
        "provider": provider,
        "region": region,
        "monthly_estimate": round(total_cost, 2),
        "breakdown": breakdown,
        "currency": "USD"
    }
