from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, DeploymentViewSet, IncidentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'deployments', DeploymentViewSet, basename='deployment')
router.register(r'incidents', IncidentViewSet, basename='incident')

urlpatterns = router.urls