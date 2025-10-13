from rest_framework import routers
from .views_api import GalaxyViewSet, StarViewSet, PlanetViewSet

router = routers.DefaultRouter()
router.register(r'galaxies', GalaxyViewSet)
router.register(r'stars', StarViewSet)
router.register(r'planets', PlanetViewSet)

urlpatterns = router.urls