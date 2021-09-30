variable "enable_server_module" {
  type        = bool
  default     = false
  description = "Choose true to build servers with a module."
}

module "server" {
  count = var.enable_server_module ? 1 : 0
  ## omitted for clarity
}