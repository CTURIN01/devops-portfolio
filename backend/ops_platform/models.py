from django.db import models


class Project(models.Model):
    """
    Represents a software service or application being tracked
    in the Deployment Operations Platform.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Deployment(models.Model):
    """
    Tracks every deployment event for a service — success, failure,
    or rollback. This is the audit trail hiring managers want to see
    you understand.
    """
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('rolled_back', 'Rolled Back'),
        ('in_progress', 'In Progress'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='deployments'
    )
    version = models.CharField(max_length=50)          # e.g. "v1.2.3" or git SHA
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    deployed_by = models.CharField(max_length=100)     # username or "ci-pipeline"
    environment = models.CharField(max_length=50, default='production')  # prod/staging
    notes = models.TextField(blank=True)
    deployed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-deployed_at']   # newest first always

    def __str__(self):
        return f"{self.project.name} — {self.version} — {self.status}"


class Incident(models.Model):
    """
    Tracks production incidents. P1 = total outage, P4 = minor.
    This model alone shows interviewers you think in SRE terms,
    not just "make it work on my machine."
    """
    SEVERITY_CHOICES = [
        ('P1', 'P1 — Critical (total outage)'),
        ('P2', 'P2 — High (major feature down)'),
        ('P3', 'P3 — Medium (degraded performance)'),
        ('P4', 'P4 — Low (minor issue)'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    severity = models.CharField(max_length=5, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    affected_project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidents'
    )
    root_cause = models.TextField(blank=True)
    resolution = models.TextField(blank=True)
    detected_at = models.DateTimeField()
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f"[{self.severity}] {self.title} — {self.status}"

# Create your models here.
