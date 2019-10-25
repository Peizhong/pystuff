import json
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets
from .models import Currency,Account,CreditAccount,Catalog,Project,Transaction
from .serializers import CurrencySerializer,AccountSerializer,CreditAccountSerializer,CatalogSerializer,ProjectSerializer,TransactionSerializer

from . import services

# Create your views here.

def chnJson(data):
    return JsonResponse({"data":data}, json_dumps_params={'ensure_ascii':False})

def update_currency(request):
    services.update_currency()
    return HttpResponse('ok')

def account_summary(request):
    r = services.account_summary()
    return chnJson(r)

def account_detail(request,account_id):
    r = services.account_detail(account_id)
    return chnJson(r)

def adjust_balance(request,account_id):
    req = json.loads(request.body)
    new_balance = req['new_balance']
    services.adjust_balance(account_id,new_balance)
    return HttpResponse('ok')

def transactions_summary(request):
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    trans_type = request.GET.get('trans_type')
    data = services.transactions_summary(date_start,date_end,trans_type)
    return HttpResponse('todo')

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class CreditAccountViewSet(viewsets.ModelViewSet):
    queryset = CreditAccount.objects.all()
    serializer_class = CreditAccountSerializer

class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date_time')
    serializer_class = TransactionSerializer

