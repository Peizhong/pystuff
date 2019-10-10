from django.contrib import admin

# Register your models here.
from .models import Currency,Account,Catalog,Project,Transaction

admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Catalog)
admin.site.register(Project)
admin.site.register(Transaction)