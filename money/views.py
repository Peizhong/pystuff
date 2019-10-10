from django.http import HttpResponse
from django.db import transaction
from rest_framework import viewsets
from .models import Currency,Account,Catalog,Project,Transaction
from .serializers import CurrencySerializer,AccountSerializer,CatalogSerializer,ProjectSerializer,TransactionSerializer
from myutils.currency import get_currency

# Create your views here.

@transaction.atomic
def update_currency(request):
    currencies = get_currency()
    db_currencies = list(Currency.objects.all())
    for c in currencies:
        cur = Currency()
        for d in db_currencies:
            if d.country == c.country:
                cur = d
                break
        cur.country = c.country
        cur.sign = c.sign
        cur.rate = c.rate
        cur.save()
    return HttpResponse('ok')
    
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

