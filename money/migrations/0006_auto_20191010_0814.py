# Generated by Django 2.2.6 on 2019-10-10 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0005_auto_20191010_0701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200)),
                ('sign', models.CharField(max_length=10)),
                ('rate', models.FloatField(default=1)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='open_balnace',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='money.Currency'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_type',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Expense'), (3, 'Income'), (5, 'Transfer'), (7, 'Adjust')], default=0),
        ),
    ]
