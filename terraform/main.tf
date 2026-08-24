terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.0"
    }
  }
}

provider "render" {
  api_key = var.render_api_key
  owner_id = var.render_owner_id
}
resource "render_postgres" "db" {
  name    = "simple-api-db"
  plan    = "free"
  region  = "frankfurt"
  version = "16"

}
resource "render_web_service" "api" {
  name   = "simple-api"
  plan   = "free"
  region = "frankfurt"


  runtime_source = {
    docker = {
      repo_url       = "https://github.com/DJMota1/Simple_CI-CD"
      branch         = "main"
      dockerfile_path = "./Dockerfile"
      context_dir    = "."
      auto_deploy    = true
    }
  }

  env_vars = {
    DATABASE_URL = {
      value = render_postgres.db.connection_info.internal_connection_string
    }
  }
}
output "api_url" {
  value = render_web_service.api.url
}