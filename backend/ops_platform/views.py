from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Project, Deployment, Incident
from .serializers import ProjectSerializer, DeploymentSerializer, IncidentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Projects.
    GET    /api/projects/              — list all projects
    POST   /api/projects/              — create a project
    GET    /api/projects/{id}/         — get one project
    PUT    /api/projects/{id}/         — update a project
    DELETE /api/projects/{id}/         — delete a project
    GET    /api/projects/{id}/health/  — custom health summary
    """
    queryset = Project.objects.prefetch_related(
        'deployments', 'incidents'
    ).all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['get'])
    def health(self, request, pk=None):
        """
        Custom endpoint: GET /api/projects/{id}/health/
        Returns a health summary for a single project —
        last deployment status, open incident count, and
        total deployment count. This is the kind of endpoint
        a real ops dashboard would call every 30 seconds.
        """
        project = self.get_object()
        last_deployment = project.deployments.first()
        open_incidents = project.incidents.filter(
            status__in=['open', 'investigating']
        ).count()
        total_deployments = project.deployments.count()
        last_5_ids = list(
            project.deployments.values_list('id', flat=True)[:5]
        )
        failed_last_5 = Deployment.objects.filter(
            id__in=last_5_ids, status='failed'
        ).count()

        return Response({
            'project': project.name,
            'last_deployment': {
                'version': last_deployment.version if last_deployment else None,
                'status': last_deployment.status if last_deployment else 'never_deployed',
                'deployed_at': last_deployment.deployed_at if last_deployment else None,
            },
            'open_incidents': open_incidents,
            'total_deployments': total_deployments,
            'failed_last_5': failed_last_5,
            'health': 'degraded' if open_incidents > 0 else 'healthy',
        })


class DeploymentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Deployments.
    GET    /api/deployments/               — list all deployments
    POST   /api/deployments/               — log a new deployment
    GET    /api/deployments/{id}/          — get one deployment
    PUT    /api/deployments/{id}/          — update a deployment
    DELETE /api/deployments/{id}/          — delete a deployment
    POST   /api/deployments/{id}/rollback/ — mark as rolled back
    GET    /api/deployments/recent/        — last 10 across all projects
    """
    queryset = Deployment.objects.select_related('project').all()
    serializer_class = DeploymentSerializer

    def get_queryset(self):
        """
        Allow filtering by project and/or status via query params.
        Example: /api/deployments/?project=1&status=failed
        This is called query param filtering — standard in production APIs.
        """
        queryset = Deployment.objects.select_related('project').all()
        project_id = self.request.query_params.get('project')
        status_filter = self.request.query_params.get('status')

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=True, methods=['post'])
    def rollback(self, request, pk=None):
        """
        Custom endpoint: POST /api/deployments/{id}/rollback/
        Marks a deployment as rolled_back and timestamps it.
        In a real system this would also trigger the actual
        rollback pipeline — here it just updates the record.
        """
        deployment = self.get_object()

        if deployment.status == 'rolled_back':
            return Response(
                {'error': 'Deployment is already rolled back.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        deployment.status = 'rolled_back'
        existing = deployment.notes or ''
        deployment.notes = existing + f'\nRolled back at {timezone.now()} by {request.user}'
        deployment.save()

        return Response(
            DeploymentSerializer(deployment).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom endpoint: GET /api/deployments/recent/
        Returns the 10 most recent deployments across ALL projects.
        The kind of feed a dashboard shows at the top of the page.
        """
        recent = Deployment.objects.select_related('project').order_by('-deployed_at')[:10]
        return Response(DeploymentSerializer(recent, many=True).data)


class IncidentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Incidents.
    GET    /api/incidents/              — list all incidents
    POST   /api/incidents/              — create an incident
    GET    /api/incidents/{id}/         — get one incident
    PUT    /api/incidents/{id}/         — update an incident
    DELETE /api/incidents/{id}/         — delete an incident
    POST   /api/incidents/{id}/resolve/ — resolve an incident
    GET    /api/incidents/open/         — all open/investigating incidents
    """
    queryset = Incident.objects.select_related('affected_project').all()
    serializer_class = IncidentSerializer

    def get_queryset(self):
        """
        Allow filtering by severity and/or status via query params.
        Example: /api/incidents/?severity=P1&status=open
        """
        queryset = Incident.objects.select_related('affected_project').all()
        severity = self.request.query_params.get('severity')
        status_filter = self.request.query_params.get('status')

        if severity:
            queryset = queryset.filter(severity=severity)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """
        Custom endpoint: POST /api/incidents/{id}/resolve/
        Marks an incident as resolved and sets resolved_at to now.
        Requires root_cause and resolution to be provided in the
        request body — you can't close an incident without explaining
        what happened and how it was fixed. Real SRE discipline.
        """
        incident = self.get_object()

        if incident.status == 'resolved':
            return Response(
                {'error': 'Incident is already resolved.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        root_cause = request.data.get('root_cause')
        resolution = request.data.get('resolution')

        if not root_cause or not resolution:
            return Response(
                {'error': 'root_cause and resolution are required to resolve an incident.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        incident.status = 'resolved'
        incident.root_cause = root_cause
        incident.resolution = resolution
        incident.resolved_at = timezone.now()
        incident.save()

        return Response(
            IncidentSerializer(incident).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def open(self, request):
        """
        Custom endpoint: GET /api/incidents/open/
        Returns all currently open or investigating incidents.
        The "war room" view — what's on fire right now.
        """
        open_incidents = Incident.objects.select_related(
            'affected_project'
        ).filter(
            status__in=['open', 'investigating']
        )
        return Response(
            IncidentSerializer(open_incidents, many=True).data
        )