# Generated by Django 2.2.5 on 2020-01-29 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BI', '0021_auto_20200129_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_chart',
            name='chart_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BI.Chart'),
        ),
        migrations.AlterField(
            model_name='user_chart',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
