# Project 4 — Kubernetes Monitoring with Prometheus & Grafana

A production-grade observability stack deployed on Kubernetes using Helm. Prometheus scrapes real-time metrics from the cluster; Grafana visualizes them on pre-built dashboards.

---

## Stack

| Tool | Role |
|---|---|
| Prometheus | Metrics collection & storage |
| Grafana | Dashboard visualization |
| Alertmanager | Alert routing & management |
| Node Exporter | Host-level CPU/memory/disk metrics |
| kube-state-metrics | Kubernetes object metrics (pods, deployments) |

---

## Architecture
Kubernetes Cluster (Minikube)
│
├── monitoring namespace
│ ├── Prometheus ← scrapes all targets every 30s
│ ├── Grafana ← visualizes metrics on dashboards
│ ├── Alertmanager ← handles alert routing
│ ├── Node Exporter ← exposes host metrics
│ └── kube-state-metrics ← exposes K8s object metrics
│
├── kube-system namespace ← scraped by Prometheus
└── default namespace ← scraped by Prometheus

text

---

## Quick Start

### Prerequisites
- Minikube running
- Helm v3+ installed
- kubectl configured

### Deploy

```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create namespace
kubectl create namespace monitoring

# Deploy full stack
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring
```

### Access Grafana

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Open http://localhost:3000

```bash
# Get admin password
kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode && echo
```

### Access Prometheus

```bash
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
```

Open http://localhost:9090

---

## What's Running

```bash
kubectl get pods -n monitoring
```
NAME READY STATUS
alertmanager-monitoring-kube-prometheus-alertmanager-0 2/2 Running
monitoring-grafana-7fcb6bbdc5-vskgm 3/3 Running
monitoring-kube-prometheus-operator-54f68d65b4-zfh94 1/1 Running
monitoring-kube-state-metrics-5957bd45bc-cn58c 1/1 Running
monitoring-prometheus-node-exporter-vtqk2 1/1 Running
prometheus-monitoring-kube-prometheus-prometheus-0 2/2 Running

text

---

## Live Metrics (Screenshots)

### Grafana — Kubernetes Cluster Dashboard
![Grafana Dashboard](screenshots/grafana-dashboard.png)

### Prometheus — Target Health
![Prometheus Targets](screenshots/prometheus-targets.png)

---

## Key Concepts Demonstrated

- **Helm** — deploying complex multi-component stacks with a single command
- **ServiceMonitors** — how Prometheus discovers scrape targets automatically in K8s
- **PromQL** — Prometheus Query Language for querying metrics
- **Observability** — the three pillars: metrics, alerting, dashboards
- **Namespace isolation** — monitoring stack separated from application workloads

---

## DevOps Concepts

This project mirrors real-world SRE/DevOps workflows:
- Production teams use `kube-prometheus-stack` as the standard monitoring solution
- Prometheus + Grafana is the most common observability stack in cloud-native environments
- Alertmanager routes alerts to Slack, PagerDuty, email, etc. in production

