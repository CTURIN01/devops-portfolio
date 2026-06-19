"""
Seed script for the Deployment Operations Platform.
Run this once via Railway console: python manage.py shell < seed_data.py
Or paste directly into: python manage.py shell

Every entry below reflects real, documented work. Nothing fabricated.
This makes the data defensible in an interview, not just decorative.
"""

from django.utils import timezone
from datetime import timedelta
from ops_platform.models import Project, Deployment, Incident

# Clear existing data for a clean seed (safe to run multiple times)
Incident.objects.all().delete()
Deployment.objects.all().delete()
Project.objects.all().delete()

now = timezone.now()

# ── PROJECTS ─────────────────────────────────────────────────────────────

devops_portfolio = Project.objects.create(
    name="DevOps Portfolio — GitOps Pipeline",
    description=(
        "Live GitOps pipeline using Argo CD v3.4.3 with selfHeal on Kubernetes. "
        "Django REST API containerized with MySQL, deployed via initContainers for "
        "dependency ordering. Full Prometheus and Grafana observability stack with "
        "PromQL dashboards and alerting rules. This API endpoint is the live deployment."
    ),
    tech_stack="Argo CD, Kubernetes, Django REST Framework, Prometheus, Grafana, Terraform, AWS, GitHub Actions",
    github_url="https://github.com/CTURIN01/devops-portfolio",
)

plaid_integration = Project.objects.create(
    name="Plaid Sandbox Integration",
    description=(
        "Complete OAuth and MFA integration flow across 4 Plaid API endpoints. "
        "Documented 7 distinct error flows with root cause, reproduction steps, "
        "and resolution path, including a webhook-gated retry pattern for "
        "PRODUCT_NOT_READY using INITIAL_UPDATE before calling transactionsSync."
    ),
    tech_stack="Node.js, Express, Plaid Link, OAuth 2.0, Webhooks, Postman",
    github_url="https://github.com/CTURIN01/plaid-sandbox-integration",
)

postgresql_db = Project.objects.create(
    name="PostgreSQL Fintech Database",
    description=(
        "Normalized fintech schema across 4 joined tables covering KYC status, "
        "multi-account balances, transaction history, and fraud flags. "
        "10 analytical queries across 6 query types, seeded with 500 mock "
        "transactions using generate_series."
    ),
    tech_stack="PostgreSQL, SQL, Docker, Bash, GitHub Actions",
    github_url="https://github.com/CTURIN01/project-postgresql",
)

# ── DEPLOYMENTS ──────────────────────────────────────────────────────────

Deployment.objects.create(
    project=devops_portfolio,
    version="v3.4.3",
    status="success",
    deployed_by="ci-pipeline",
    environment="production",
    notes=(
        "Argo CD GitOps sync from GitHub to Kubernetes cluster. selfHeal enabled, "
        "auto-pruning active. All manifests validated pre-deploy via GitHub Actions."
    ),
)

Deployment.objects.create(
    project=devops_portfolio,
    version="v3.4.2",
    status="rolled_back",
    deployed_by="ci-pipeline",
    environment="production",
    notes=(
        "Intentional MySQL pod failure injected to validate self-healing. "
        "Readiness probe detected failure in 10 seconds, Argo CD selfHeal "
        "triggered automatic recovery, full restoration in 23 seconds."
    ),
)

Deployment.objects.create(
    project=devops_portfolio,
    version="railway-prod-1",
    status="success",
    deployed_by="ctruin01",
    environment="production",
    notes="Deployed Django REST API to Railway with SQLite, gunicorn, and whitenoise static file handling.",
)

Deployment.objects.create(
    project=plaid_integration,
    version="v1.2.0",
    status="success",
    deployed_by="ctruin01",
    environment="sandbox",
    notes="Implemented webhook-gated retry for PRODUCT_NOT_READY error using INITIAL_UPDATE event listener.",
)

Deployment.objects.create(
    project=postgresql_db,
    version="v1.0.0",
    status="success",
    deployed_by="ctruin01",
    environment="staging",
    notes="Seeded 500 mock transactions, validated all 10 analytical queries with EXPLAIN ANALYZE.",
)

# ── INCIDENTS ────────────────────────────────────────────────────────────

Incident.objects.create(
    title="MySQL pod failure — readiness probe validation",
    severity="P2",
    status="resolved",
    affected_project=devops_portfolio,
    root_cause=(
        "Intentional pod deletion to test self-healing infrastructure. "
        "MySQL pod terminated, dependent Django pod's initContainer began "
        "failing readiness checks against the database connection."
    ),
    resolution=(
        "Argo CD selfHeal detected drift from desired state and triggered "
        "automatic pod recreation. Readiness probe confirmed failure at 10 seconds. "
        "Full service restoration confirmed at 23 seconds via Grafana metrics "
        "showing HTTP request gap during the recovery window."
    ),
    detected_at=now - timedelta(days=3, hours=2),
    resolved_at=now - timedelta(days=3, hours=2) + timedelta(seconds=23),
)

Incident.objects.create(
    title="Plaid /transactions/sync returning empty results",
    severity="P3",
    status="resolved",
    affected_project=plaid_integration,
    root_cause=(
        "Async initialization gap of 8 to 12 seconds between account verification "
        "and transaction data becoming available. Calling transactionsSync "
        "immediately after Link exchange returned empty results before Plaid "
        "finished populating transaction data server-side."
    ),
    resolution=(
        "Implemented a webhook-gated retry pattern. Instead of calling sync "
        "immediately, the integration now waits for the INITIAL_UPDATE webhook "
        "event, which fires once transaction data is confirmed ready, then calls "
        "transactionsSync. Eliminated the failure with zero recurrence after the fix."
    ),
    detected_at=now - timedelta(days=14, hours=5),
    resolved_at=now - timedelta(days=14, hours=3),
)

Incident.objects.create(
    title="Railway deployment crash — MySQL connection in SQLite environment",
    severity="P1",
    status="resolved",
    affected_project=devops_portfolio,
    root_cause=(
        "Original settings.py was hardcoded to MySQL with no environment-based "
        "fallback. Railway's environment has no MySQL socket available, causing "
        "OperationalError on every startup attempt. A committed venv/ folder also "
        "contained Windows-compiled MySQL binaries incompatible with Railway's "
        "Linux build environment."
    ),
    resolution=(
        "Rewrote settings.py using dj_database_url with a SQLite default for "
        "Railway and MySQL fallback for local development. Added .dockerignore "
        "to exclude venv/ and source/ from the build context. Configured gunicorn "
        "as the start command via Procfile."
    ),
    detected_at=now - timedelta(hours=18),
    resolved_at=now - timedelta(hours=2),
)

print("Seed complete.")
print(f"Projects: {Project.objects.count()}")
print(f"Deployments: {Deployment.objects.count()}")
print(f"Incidents: {Incident.objects.count()}")
