# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Document(models.Model):

    class Meta:
        db_table = 'documents'

    FILE_CHOICES = (
        ('B', 'Balance'),
        ('T', 'Transaction'),
    )
    
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    file_type = models.CharField(choices=FILE_CHOICES, max_length=1, default='B')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class DeleteDataHistory(models.Model):

    class Meta:
        db_table = 'delete_data_history'
    
    reason = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    deleted_at = models.DateTimeField(auto_now_add=True)


class Balance(models.Model):

    class Meta:
        db_table = 'tradar_balances'
    
    fund = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    ccy = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class Transactions(models.Model):

    class Meta:
        db_table = 'tradar_transactions'
    
    trade = models.IntegerField(blank=False)
    fund = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    security_type = models.CharField(max_length=255)
    ticker = models.CharField(max_length=255)
    isin = models.CharField(max_length=255)
    cusip = models.CharField(max_length=255)
    sedol = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)
    ccy = models.CharField(max_length=255)
    settles = models.DateField(auto_now_add=True)
    account = models.CharField(max_length=255)
    cash_flow = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class ClientData(models.Model):

    class Meta:
        db_table = 'client_data'
    fund = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    file_type = models.CharField(max_length=1)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=255)
    settle_date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=255)