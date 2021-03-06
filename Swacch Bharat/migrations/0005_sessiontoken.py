# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Swacch Bharat', '0004_auto_20170814_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Swacch Bharat.UserModel')),
            ],
        ),
    ]
