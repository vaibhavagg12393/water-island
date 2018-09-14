# -*- coding: utf-8 -*-

from django import forms

from home.models import Document, DeleteDataHistory


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('description', 'document', 'file_type')


class DeleteDataHistoryForm(forms.ModelForm):

    class Meta:
        model = DeleteDataHistory
        fields = ('name', 'reason')