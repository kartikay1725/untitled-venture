provider "aws" {
  region = var.aws_region
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "mvpgenie-cluster"
  cluster_version = "1.29"
  subnets         = var.private_subnets
  vpc_id          = var.vpc_id
  node_groups = {
    default = {
      desired_capacity = 3
      max_capacity     = 10
      min_capacity     = 3
      instance_types   = ["t3.medium"]
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_secret" "mvpgenie_secrets" {
  metadata {
    name = "mvpgenie-secrets"
  }
  data = {
    DATABASE_URL = base64encode("postgresql+asyncpg://user:pass@db:5432/mvpgenie")
    SECRET_KEY   = base64encode("super-secret-key")
  }
}
