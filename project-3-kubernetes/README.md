# Project 3 — Kubernetes Deployment

## Overview
Deployed a containerized web application to a local Kubernetes cluster using Minikube. Demonstrates core K8s concepts: Deployments, Services, and horizontal pod scaling.

## Tech Stack
- Kubernetes v1.35.1
- Minikube v1.38.1
- kubectl v1.34.1
- Docker driver

## What I Built
- **Deployment** — 2-replica pod deployment with rolling update strategy
- **Service** — NodePort service exposing the app on port 30080
- **Scaling** — Scaled 2 → 5 replicas live with zero downtime

## Commands
```bash
minikube start --driver=docker
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl scale deployment django-api --replicas=5
kubectl get pods -w
```
