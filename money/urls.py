from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'catalogs', views.CatalogViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'transactions', views.TransactionViewSet)

app_name = 'money'
urlpatterns = router.urls