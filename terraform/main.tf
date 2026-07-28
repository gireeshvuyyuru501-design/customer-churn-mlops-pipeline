terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_container" "churn_api" {
  name  = "churn-mlops-api-tf"
  image = "churn-mlops-api:latest"

  ports {
    internal = 8000
    external = 8000
  }

  restart = "unless-stopped"
}

output "api_url" {
  value = "http://localhost:8000"
}