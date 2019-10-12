from django.db import models

# Create your models here.
# python manage.py makemigrations money
# python manage.py migrate

class Currency(models.Model):
    country = models.CharField(max_length=200)
    country_zh = models.CharField(max_length=200, null=True, blank=True)
    sign = models.CharField(max_length=10)
    rate = models.FloatField(default=1)
    enabled = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class Account(models.Model):
    ACCOUNT_TYPE = (
        (0, 'None'),
        (1, '现金'),
        (3, '借记卡'),
        (5, '信用卡'),
    )
    account_name = models.CharField(max_length=200)
    account_type = models.IntegerField(default=0, choices=ACCOUNT_TYPE)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    open_balnace = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    remark = models.CharField(max_length=2048, null=True, blank=True)
    
    def __str__(self):
        return "%s_%s"%(self.get_account_type_display(),self.account_name)

class CreditAccount(Account):
    credit_limit = models.FloatField(default=0)
    billing_day = models.IntegerField(default=0)
    billing_cycle = models.IntegerField(default=0)
    include_today = models.BooleanField(default=False)

class Catalog(models.Model):
    catalog_name = models.CharField(max_length=200)
    parent_id = models.IntegerField(default=0)
    logo = models.IntegerField(default=0)

    def __str__(self):
        return self.catalog_name

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    remark = models.CharField(max_length=2048, null=True, blank=True)
    
    def __str__(self):
        return self.project_name

class Transaction(models.Model):
    class Meta:
        ordering = ['-date_time']
    
    TRANS_TYPE = (
        (0, 'None'),
        (1, '支出'),
        (3, '收入'),
        (5, '转账'),
        (7, '调整')
    )
    trans_type = models.IntegerField(default=0, choices=TRANS_TYPE)
    out_account = models.ForeignKey(Account, on_delete=models.DO_NOTHING,related_name='out_account_id', null=True, blank=True)
    in_account = models.ForeignKey(Account, on_delete=models.DO_NOTHING,related_name='id_account_id', null=True, blank=True)
    out_amt = models.FloatField(default=0)
    in_amt = models.FloatField(default=0)
    trans_rate = models.FloatField(default=1)
    date_time = models.DateTimeField()
    catalog = models.ForeignKey(Catalog, on_delete=models.DO_NOTHING, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True, blank=True)
    remark = models.CharField(max_length=2048, null=True, blank=True)

    def __str__(self):
        return '%s/%s/%s %s'%(self.date_time.year,self.date_time.month,self.date_time.day,self.remark)