# Troubleshooting Notes

## Pod not starting
- Check events: `kubectl describe pod <pod-name>`
- Check logs: `kubectl logs <pod-name>`
- Verify image name and tag are correct

## Service not reachable
- Confirm service selector matches pod labels
- Check port mapping in service spec
- Run: `kubectl get endpoints <service-name>`

## Resource limits
- OOMKilled means pod exceeded memory limit
- Increase `resources.limits.memory` in deployment spec
