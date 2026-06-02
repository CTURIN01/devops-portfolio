# devops-portfolio

A hands-on DevOps portfolio demonstrating real infrastructure skills across CI/CD pipelines, Infrastructure as Code, Kubernetes orchestration, GitOps deployment, monitoring, and incident management. All projects are fully functional and designed to reflect production-grade practices.

---

## Live GitOps Pipeline — ArgoCD + Kubernetes

![ArgoCD Resource Graph](argocd-dashboard.png)

This repo powers a **live GitOps pipeline** running on Kubernetes via ArgoCD:

- **App Health:** ✅ Healthy
- **Sync Status:** ✅ Synced to `main`
- **Resources:** ConfigMap, Namespace, Service, Deployment, 2 Pods
- **Pipeline:** `git push` → ArgoCD detects diff → auto-syncs to Kubernetes

ArgoCD watches this repo's `k8s/` folder. Any change pushed to `main` is automatically applied to the cluster — no manual `kubectl apply` required.

---

## Projects

### Project 1 — CI/CD Pipeline
**Directory:** `project-5-cicd/`

Automated build and deployment pipeline. Covers:
- Continuous integration with automated testing
- Docker image build and push
- Deployment triggers on merge to main

---

### Project 2 — Infrastructure Provisioning (Terraform)
**Directory:** `project-2-terraform/`

Infrastructure as Code using Terraform to provision cloud resources:
- VPC, subnets, and security groups
- EC2/compute resource provisioning
- State management and modular design

---

### Project 3 — Kubernetes Orchestration
**Directory:** `project-3-kubernetes/`

Container orchestration with Kubernetes:
- Deployment manifests with replica management
- Service discovery and load balancing
- ConfigMaps and resource limits

---

### Project 4 — Monitoring & Observability
**Directory:** `project-4-monitoring/`

Full observability stack:
- Metrics collection and dashboards (Grafana)
- Alerting rules and thresholds
- Application and infrastructure monitoring

---

### Project 5 — AIOps
**Directory:** `project-5-cicd/`

Intelligent operations tooling:
- Automated anomaly detection
- Log analysis and pattern recognition

---

### Project 6 — Hybrid Incident Runbook
**Directory:** `project-6-hybrid-incident-runbook/`

Production-grade incident response documentation:
- Step-by-step runbooks for common failure scenarios
- Escalation paths and rollback procedures
- Post-incident review templates

---

## GitOps Architecture
Developer pushes to main
│
▼
GitHub (source of truth)
│
▼
ArgoCD detects diff between Git state and cluster state
│
▼
ArgoCD syncs — applies manifests to Kubernetes
│
▼
Kubernetes runs the updated workloads

text

### Repo Structure
devops-portfolio/
├── k8s/ # Raw Kubernetes manifests
│ ├── namespace.yaml
│ ├── deployment.yaml
│ ├── service.yaml
│ └── configmap.yaml
├── helm/ # Helm chart (templated)
│ └── devops-app/
│ ├── Chart.yaml
│ ├── values.yaml
│ └── templates/
├── argocd/ # ArgoCD Application definitions
│ ├── application.yaml
│ └── app-of-apps.yaml
├── project-2-terraform/ # IaC — Terraform
├── project-3-kubernetes/ # Kubernetes configs
├── project-4-monitoring/ # Grafana + alerting
├── project-5-cicd/ # CI/CD pipeline
├── project-6-hybrid-incident-runbook/
├── argocd-notes.md
├── deployment-checklist.md
└── gitops-workflow.md

text

---

## Stack

| Tool            | Purpose                    |
|----------------|----------------------------|
| Kubernetes      | Container orchestration    |
| ArgoCD          | GitOps continuous delivery |
| Helm            | Kubernetes package management |
| Terraform       | Infrastructure as Code     |
| Docker          | Containerization           |
| Grafana         | Monitoring & dashboards    |
| GitHub Actions  | CI/CD automation           |
| AWS             | Cloud infrastructure       |

---

## How to Run Locally

### Prerequisites
- Docker Desktop running
- minikube installed
- kubectl installed

### Start the Cluster

```bash
minikube start --driver=docker --cpus=2 --memory=4096
```

### Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd -w
```

### Access ArgoCD UI

```bash
# In a separate terminal
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl get secret argocd-initial-admin-secret \
  -n argocd \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

Open **https://localhost:8080** — login with `admin` and the password above.

### Deploy the App

```bash
kubectl apply -f argocd/application.yaml
```

ArgoCD will sync your app from this repo automatically.

---

## Deployment Checklist

See [`deployment-checklist.md`](deployment-checklist.md) for pre, during, and post-deployment steps.

---

## Author

**Chris Turin**  
DevOps Engineer | FL  
[GitHub: CTURIN01](https://github.com/CTURIN01)
