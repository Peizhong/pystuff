# Generated by Django 2.0.5 on 2018-07-06 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_auto_20180705_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='user_id',
            new_name='user',
        ),
    ]
