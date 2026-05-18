# Grafana + Prometheus Notes

## Accessing Grafana
- Default port: 3000
- Default login: admin / admin (change immediately)

## Adding Prometheus as a data source
1. Go to Configuration > Data Sources
2. Select Prometheus
3. Set URL to http://prometheus:9090
4. Click Save & Test

## Common dashboard panels
- CPU usage: `rate(container_cpu_usage_seconds_total[5m])`
- Memory usage: `container_memory_usage_bytes`
- Pod restarts: `kube_pod_container_status_restarts_total`
