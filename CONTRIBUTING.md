# Contributing

Thank you for checking out this project! Here's how to run it locally and contribute.

## Prerequisites

Make sure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [ArgoCD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/)

## Run Locally

### 1. Start Minikube

```bash
minikube start
```

### 2. Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --for=condition=available --timeout=120s deployment/argocd-server -n argocd
```

### 3. Access the ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Then open [https://localhost:8080](https://localhost:8080)

Default username: `admin`

Get the password:
```bash
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. Apply the Kubernetes Manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 5. Verify Everything is Running

```bash
kubectl get pods -n argocd
kubectl get all
```

## Making Changes

1. Fork the repo and create a new branch: `git checkout -b feat/your-feature`
2. Make your changes
3. Commit with a clear message: `git commit -m "feat: describe your change"`
4. Push and open a Pull Request

## CI/CD

Every push to `main` triggers two GitHub Actions workflows:

- **CI Pipeline** — runs linting and build checks
- **Validate K8s Manifests** — runs `yamllint` on all Kubernetes YAML files

Both must pass before merging.
