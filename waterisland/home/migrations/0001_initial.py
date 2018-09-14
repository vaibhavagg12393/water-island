# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-13 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade', models.IntegerField()),
                ('type', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('security_type', models.CharField(max_length=255)),
                ('ticker', models.CharField(max_length=255)),
                ('isin', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('settles', models.DateField(auto_now_add=True)),
                ('cash_flow', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'db_table': 'tradar_balances',
            },
        ),
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund', models.CharField(max_length=255)),
                ('institution', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=1)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('currency', models.CharField(max_length=255)),
                ('settle_date', models.DateField(auto_now_add=True)),
                ('details', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'client_data',
            },
        ),
        migrations.CreateModel(
            name='DeleteDataHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('deleted_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'delete_data_history',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('file_type', models.CharField(choices=[('B', 'Balance'), ('T', 'Transaction')], default='B', max_length=1)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'documents',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade', models.IntegerField()),
                ('fund', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('security_type', models.CharField(max_length=255)),
                ('ticker', models.CharField(max_length=255)),
                ('isin', models.CharField(max_length=255)),
                ('cusip', models.CharField(max_length=255)),
                ('sedol', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('ccy', models.CharField(max_length=255)),
                ('settles', models.DateField(auto_now_add=True)),
                ('account', models.CharField(max_length=255)),
                ('cash_flow', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'db_table': 'tradar_transactions',
            },
        ),
    ]
