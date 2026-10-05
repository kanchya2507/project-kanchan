# Remote state in S3. The bucket must exist BEFORE `terraform init`
# (see README "Remote state bootstrap"). Backend blocks cannot use variables,
# so edit the values below directly.
terraform {
  backend "s3" {
    bucket       = "tfstate-652978908837-us-east-1" # must be globally unique
    key          = "fastapi-ecs/dev/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true ## S3 native locking, no DynamoDB table needed
  }
}
