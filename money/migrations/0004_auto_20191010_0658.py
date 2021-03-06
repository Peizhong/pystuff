# Generated by Django 2.2.6 on 2019-10-10 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0003_auto_20191010_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='catalog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='money.Catalog'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='in_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='id_account_id', to='money.Account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='out_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='out_account_id', to='money.Account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_rate',
            field=models.FloatField(default=1),
        ),
    ]
