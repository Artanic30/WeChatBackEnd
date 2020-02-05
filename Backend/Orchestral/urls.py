from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register(r'absence', views.AbsenceViewSet, base_name='absence')
router.register(r'manager', views.ManagerViewSet, base_name='manager')
router.register(r'account', views.AccountsViewSet, base_name='account')


urlpatterns = router.urls
