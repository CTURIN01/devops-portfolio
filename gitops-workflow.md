# GitOps Workflow

## Overview
This repo uses a GitOps model: Git is the single source of truth for all
infrastructure and application state. ArgoCD watches this repo and
automatically syncs any changes to the Kubernetes cluster.

## The Pipeline
Developer pushes to main
|
v
GitHub (source of truth)
|
v
ArgoCD detects diff between Git state and cluster state
|
v
ArgoCD syncs — applies manifests to Kubernetes
|
v
Kubernetes runs the updated workloads

text

## Repo Structure
devops-portfolio/
├── k8s/ # Raw Kubernetes manifests
│ ├── namespace.yaml
│ ├── deployment.yaml
│ ├── service.yaml
│ └── configmap.yaml
├── helm/ # Helm chart (templated version of k8s/)
│ └── devops-app/
│ ├── Chart.yaml
│ ├── values.yaml
│ └── templates/
├── argocd/ # ArgoCD Application definitions
│ ├── application.yaml # Single app pointing at k8s/
│ └── app-of-apps.yaml # App of Apps pattern
└── gitops-workflow.md # This file

text

## How to Deploy a Change

1. Edit any file in `k8s/` or `helm/`
2. Commit and push to `main`
3. ArgoCD detects the change within 3 minutes (default polling interval)
4. ArgoCD applies the diff to the cluster automatically
5. Verify in ArgoCD UI or via CLI:

```bash
argocd app get devops-app
argocd app sync devops-app   # manual trigger if needed
```

## How to Rollback

```bash
# List previous sync history
argocd app history devops-app

# Roll back to a specific revision
argocd app rollback devops-app <revision-number>
```

## Drift Detection
If someone manually edits the cluster with `kubectl`, ArgoCD will detect
the drift and either alert (manual sync) or auto-correct it (selfHeal: true).
