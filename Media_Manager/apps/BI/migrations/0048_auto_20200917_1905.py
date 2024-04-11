# Generated by Django 2.2.5 on 2020-09-17 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BI', '0047_auto_20200916_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auth_subgroup_permissions',
            name='permission_id',
        ),
        migrations.RemoveField(
            model_name='auth_subgroup_permissions',
            name='subgroup_id',
        ),
        migrations.RemoveField(
            model_name='auth_user_subgroup',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='auth_user_subgroup',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='chart_group',
            name='chart',
        ),
        migrations.RemoveField(
            model_name='dashboard_group',
            name='dashboard',
        ),
        migrations.DeleteModel(
            name='Auth_Subgroup',
        ),
        migrations.DeleteModel(
            name='Auth_Subgroup_permissions',
        ),
        migrations.DeleteModel(
            name='Auth_User_Subgroup',
        ),
        migrations.DeleteModel(
            name='Chart_Group',
        ),
        migrations.DeleteModel(
            name='Dashboard_Group',
        ),
    ]
