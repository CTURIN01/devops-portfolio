# Project 2 — AWS EC2 Provisioning with Terraform

## Overview
Provisioned a live AWS EC2 t2.micro instance using Infrastructure as Code (IaC) with Terraform.

## Tech Stack
- Terraform v5.100.0
- AWS EC2 (t2.micro, Amazon Linux 2)
- AWS Provider (HashiCorp)

## What I Built
- Defined cloud infrastructure as code in `main.tf`
- Used `terraform plan` to preview changes before applying
- Provisioned a real EC2 instance in `us-east-1d` in under 30 seconds
- Captured live instance state and public IP via `terraform show` and `terraform output`

## Key Terraform Commands Used
| Command | Purpose |
|---------|---------|
| `terraform init` | Initialize provider plugins |
| `terraform plan` | Dry-run preview of infrastructure changes |
| `terraform apply` | Provision real AWS resources |
| `terraform show` | Inspect live state of deployed resources |
| `terraform destroy` | Tear down infrastructure cleanly |

## Instance Details (Deployed)
- **Instance ID:** i-09168db06145e1fd5
- **Type:** t2.micro (Free Tier)
- **Region:** us-east-1d
- **Public IP:** 54.80.78.200
- **AMI:** ami-0c02fb55956c7d316 (Amazon Linux 2)
