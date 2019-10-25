import datetime
from django.db import connection,transaction
from .models import Currency,Account,CreditAccount,Catalog,Project,Transaction
from myutils.currency import get_currency

def account_summary():
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
        return r

def account_detail(account_id):
    # 计算余额
    sql = """select id,
       account_name,
       open_balnace
       + ifnull((select sum(in_amt*trans_rate) from money_transaction where money_transaction.in_account_id = money_account.id),0)
       - ifnull((select sum(out_amt*trans_rate) from money_transaction where money_transaction.out_account_id = money_account.id),0) balance
    from money_account where id = %s"""
    with connection.cursor() as c:
        c.execute(sql,[account_id])
        columns = [col[0] for col in c.description]
        row = c.fetchone()
        r = dict(zip(columns, row))
        return r

def adjust_balance(account_id,new_balance):
    try:
        account = Account.objects.get(pk=account_id)
    except Account.DoesNotExist:
        return
    else:
        detail = account_detail(account_id)
        diff = new_balance - detail['balance']
        if diff == 0:
            return
        ## 创建一条支出/收入
        trans = Transaction()
        trans.trans_type = 7
        trans.remark = '调整收支'
        trans.currency = account.currency
        if diff > 0:
            trans.in_account = account
            trans.in_amt = diff
        elif diff < 0:
            trans.out_account = account
            trans.out_amt = diff * -1
        trans.date_time = datetime.datetime.now()
        trans.save()

def transactions_summary(date_start,date_end,trans_type):
    query = Transaction.objects
    if date_start:
        p_date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
        query = query.filter(date_time__gte=p_date_start)
        if date_end:
            p_date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
            query = query.filter(date_time__lte=p_date_end)
    data = list(query.all())
    return data

@transaction.atomic
def update_currency():
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