from rest_framework import viewsets
from .models import Currency,Account,Catalog,Project,Transaction
from .serializers import CurrencySerializer,AccountSerializer,CatalogSerializer,ProjectSerializer,TransactionSerializer
from myutils.currency import update_currency

# Create your views here.

def init_currency():
    currency = update_currency()
    l = list()
    for c in currency:
        l.append(Currency(country=c.code,rate=c.rate))
    Currency.objects.bulk_create(l)
    
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

