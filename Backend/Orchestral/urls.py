from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

# router.register(r'game', views.GameViewSet, base_name='game')


urlpatterns = router.urls
