# Generated by Django 2.2.5 on 2020-08-18 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BI', '0036_auto_20200818_0448'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='order_id',
            field=models.CharField(default='0', max_length=10),
        ),
        migrations.AddField(
            model_name='user_dashboard',
            name='order_id',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
