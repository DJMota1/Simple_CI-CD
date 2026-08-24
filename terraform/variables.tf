variable "render_api_key" {
  description = "API key do Render para autenticação"
  type        = string
  sensitive   = true
}

variable "render_owner_id" {
  description = "ID do owner/workspace no Render"
  type        = string
}