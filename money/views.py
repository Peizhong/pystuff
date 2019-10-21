import datetime
from django.http import HttpResponse,JsonResponse
from django.db import connection,transaction
from rest_framework import viewsets
from .models import Currency,Account,CreditAccount,Catalog,Project,Transaction
from .serializers import CurrencySerializer,AccountSerializer,CreditAccountSerializer,CatalogSerializer,ProjectSerializer,TransactionSerializer
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
        cur.country_zh = c.country_zh
        cur.sign = c.sign
        cur.rate = c.rate
        cur.save()
    return HttpResponse('ok')

def account_summary(request):
    # 计算余额
    sql = """select id,
       account_name,
       open_balnace
       + ifnull((select sum(in_amt*trans_rate) from money_transaction where money_transaction.in_account_id = money_account.id),0)
       - ifnull((select sum(out_amt*trans_rate) from money_transaction where money_transaction.out_account_id = money_account.id),0) balance
    from money_account where enabled = 1 order by id"""
    with connection.cursor() as c:
        c.execute(sql)
        columns = [col[0] for col in c.description]
        r = [dict(zip(columns, row)) for row in c.fetchall()]
        return JsonResponse({"data":r})

def transactions_summary(request):
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    trans_type = request.GET.get('trans_type')
    query = Transaction.objects
    if date_start:
        p_date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
        query = query.filter(date_time__gte=p_date_start)
        if date_end:
            p_date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
            query = query.filter(date_time__lte=p_date_end)
    data = list(query.all())
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

