from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register(r'absence', views.AbsenceViewSet, basename='absence')
router.register(r'manager', views.ManagerViewSet, basename='manager')
router.register(r'account', views.AccountsViewSet, basename='account')


urlpatterns = router.urls
