from rest_framework import serializers
from .models import Project, Deployment, Incident


class DeploymentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source='project.name',
        read_only=True
    )

    class Meta:
        model = Deployment
        fields = [
            'id',
            'project',
            'project_name',
            'version',
            'status',
            'deployed_by',
            'environment',
            'notes',
            'deployed_at',
        ]


class IncidentSerializer(serializers.ModelSerializer):
    affected_project_name = serializers.CharField(
        source='affected_project.name',
        read_only=True,
        allow_null=True
    )
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        fields = [
            'id',
            'title',
            'severity',
            'status',
            'affected_project',
            'affected_project_name',
            'root_cause',
            'resolution',
            'detected_at',
            'resolved_at',
            'duration_minutes',
            'created_at',
        ]

    def get_duration_minutes(self, obj):
        if obj.resolved_at and obj.detected_at:
            delta = obj.resolved_at - obj.detected_at
            return round(delta.total_seconds() / 60)
        return None


class ProjectSerializer(serializers.ModelSerializer):
    recent_deployments = serializers.SerializerMethodField()
    open_incidents = serializers.SerializerMethodField()
    last_deployment_status = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'tech_stack',
            'github_url',
            'last_deployment_status',
            'recent_deployments',
            'open_incidents',
            'created_at',
        ]

    def get_recent_deployments(self, obj):
        deployments = obj.deployments.all()[:5]
        return DeploymentSerializer(deployments, many=True).data

    def get_open_incidents(self, obj):
        incidents = obj.incidents.filter(
            status__in=['open', 'investigating']
        )
        return IncidentSerializer(incidents, many=True).data

    def get_last_deployment_status(self, obj):
        last = obj.deployments.first()
        if last:
            return last.status
        return 'never_deployed'