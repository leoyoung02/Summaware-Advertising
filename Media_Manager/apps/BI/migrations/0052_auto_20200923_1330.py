# Generated by Django 2.2.5 on 2020-09-23 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('BI', '0051_auto_20200917_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='assigned_dashboards',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chart',
            name='group_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dashboard',
            name='group_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_chart',
            name='assigned_dashboards',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_chart',
            name='group_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_dashboard',
            name='group_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
            preserve_default=False,
        ),
    ]
