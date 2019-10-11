from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'credit_accounts', views.CreditAccountViewSet)
router.register(r'catalogs', views.CatalogViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'transactions', views.TransactionViewSet)

app_name = 'money'

urlpatterns = [
    path('update_currency/', views.update_currency, name='update_currency'),
    path('account_summary/', views.account_summary, name='account_summary'),
    path('transactions_summary/', views.transactions_summary, name='transactions_summary')
]
urlpatterns.extend(router.urls)