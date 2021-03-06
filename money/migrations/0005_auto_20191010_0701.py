# Generated by Django 2.2.6 on 2019-10-10 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0004_auto_20191010_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='money.Project'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_type',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Expense'), (3, 'Income'), (5, 'Transfer')], default=0),
        ),
    ]
