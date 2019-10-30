from django.contrib import admin
from .models import Currency,Account,CreditAccount,Catalog,Project,Transaction

# Register your models here.

admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(CreditAccount)
admin.site.register(Catalog)
admin.site.register(Project)
admin.site.register(Transaction)