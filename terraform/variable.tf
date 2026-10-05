############ General ############
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "fastapi"
}

variable "environment" {
  type    = string
  default = "dev"
}

############ Network ############
variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "az_count" {
  description = "Number of Availability Zones (ALB needs at least 2)"
  type        = number
  default     = 2
}

variable "enable_nat_gateway" {
  description = "true = ECS tasks in PRIVATE subnets behind NAT (diagram design). false = tasks in PUBLIC subnets with public IPs (cheapest, no NAT)."
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "true = one shared NAT (cheaper). false = one NAT per AZ (HA, 2x NAT cost)."
  type        = bool
  default     = true
}

############ Container / Task ############
variable "container_name" {
  type    = string
  default = "fast-api"
}

variable "container_port" {
  type    = number
  default = 8000
}

variable "container_image" {
  description = "kanchya2507/fastapi-app:latest"
  type        = string
}

variable "dockerhub_secret_arn" {
  description = "Only for a PRIVATE Docker Hub repo: ARN of a Secrets Manager secret with {\"username\":\"...\",\"password\":\"<access token>\"}. Empty = public image."
  type        = string
  default     = ""
}

variable "health_check_path" {
  type    = string
  default = "/health"
}

variable "task_cpu" {
  description = "Fargate CPU units (256 = 0.25 vCPU)"
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "Fargate memory in MiB"
  type        = number
  default     = 512
}

variable "environment_variables" {
  description = "Plain env vars for the container. Use Secrets Manager/SSM for secrets."
  type        = map(string)
  default     = {}
}

variable "use_fargate_spot" {
  description = "~70% cheaper compute but tasks can be interrupted. Fine for dev."
  type        = bool
  default     = false
}

############ Scaling ############
variable "desired_count" {
  type    = number
  default = 2
}

variable "min_capacity" {
  type    = number
  default = 2
}

variable "max_capacity" {
  type    = number
  default = 6
}

variable "cpu_target_percent" {
  type    = number
  default = 60
}

variable "requests_per_target" {
  type    = number
  default = 500
}

############ DNS / TLS (optional) ############
variable "domain_name" {
  description = "e.g. api.example.com. Leave empty for HTTP-only on the ALB DNS name."
  type        = string
  default     = ""
}

variable "hosted_zone_name" {
  description = "Existing Route 53 hosted zone, e.g. example.com (required if domain_name is set)"
  type        = string
  default     = ""
}

############ Observability / Cost ############
variable "log_retention_days" {
  type    = number
  default = 14
}

variable "enable_container_insights" {
  description = "Adds CloudWatch custom-metric cost. Keep false unless needed."
  type        = bool
  default     = false
}

variable "alarm_email" {
  description = "Email for alarms and budget alerts. Empty = no subscription/budget created."
  type        = string
  default     = ""
}

variable "monthly_budget_usd" {
  type    = string
  default = "100"
}
