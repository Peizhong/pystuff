from django.db import models

# Create your models here.
# python manage.py makemigrations money
# python manage.py migrate

class Currency(models.Model):
    country = models.CharField(max_length=200)
    sign = models.CharField(max_length=10)
    rate = models.FloatField(default=1)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class Account(models.Model):
    ACCOUNT_TYPE = (
        (0, 'None'),
        (1, 'Cash'),
        (3, 'Debit'),
        (5, 'Credit'),
    )
    account_name = models.CharField(max_length=200)
    account_type = models.IntegerField(default=0, choices=ACCOUNT_TYPE)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    open_balnace = models.FloatField(default=0)
    remark = models.CharField(max_length=2048, null=True, blank=True)
    
    def __str__(self):
        return self.account_name

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
