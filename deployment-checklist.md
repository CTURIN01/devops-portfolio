# Deployment Checklist

## Pre-Deployment
- [ ] All tests passing in CI pipeline
- [ ] Docker image builds cleanly locally
- [ ] Environment variables verified in `.env` / secrets manager
- [ ] Database migrations reviewed and tested
- [ ] Rollback plan documented

## Deployment
- [ ] Pull latest from main: `git pull origin main`
- [ ] Build and push Docker image: `docker build -t app:latest .`
- [ ] Apply infrastructure changes: `terraform plan` → `terraform apply`
- [ ] Deploy to Kubernetes: `kubectl apply -f k8s/`
- [ ] Verify pods are running: `kubectl get pods`
- [ ] Check service endpoints: `kubectl get svc`

## Post-Deployment
- [ ] Smoke test critical endpoints
- [ ] Check application logs: `kubectl logs -f <pod>`
- [ ] Confirm metrics visible in Grafana
- [ ] No spike in error rate in Prometheus
- [ ] Notify team deployment is complete

## Rollback Steps
1. Identify last stable image tag
2. `kubectl set image deployment/app app=image:previous-tag`
3. Verify pods stabilize: `kubectl rollout status deployment/app`
4. Document what went wrong and open postmortem
