# DevOps Troubleshooting Notes

## Docker
- Container stuck restarting: `docker logs <container>` then `docker inspect` for restart policy.
- Image not updating: `docker compose pull` then `docker compose up -d --force-recreate`.

## Kubernetes
- Pod CrashLoopBackOff: `kubectl describe pod <name>` and `kubectl logs <name>`.
- Stuck terminating: check finalizers, then `kubectl delete pod <name> --grace-period=0 --force`.

## Terraform
- State lock: clear via `terraform force-unlock <LOCK_ID>` after verifying nothing is running.
- Drift: run `terraform plan` regularly and document any manual changes.

## CI/CD
- Pipeline flaky: separate infra issues (network, rate limits) from test issues; rerun job with debug logging.
