# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-23 21:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0002_auto_20190823_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='active_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='active_jobs', to='login_reg_app.User'),
        ),
        migrations.AlterField(
            model_name='job',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs_posted', to='login_reg_app.User'),
        ),
    ]
