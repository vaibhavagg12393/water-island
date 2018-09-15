# -*- coding: utf-8 -*-

from django import forms

from home.models import Document, DeleteDataHistory


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('description', 'document', 'file_type')
    
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['document'].widget.attrs.update({'class' : 'select-file'})


class DeleteDataHistoryForm(forms.ModelForm):

    class Meta:
        model = DeleteDataHistory
        fields = ('name', 'reason')