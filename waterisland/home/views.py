# -*- coding: utf-8 -*-

import shutil

from django.conf import settings
from django.shortcuts import render, redirect

from home.forms import DeleteDataHistoryForm, DocumentForm
from home.models import Balance, ClientData, Document, Transactions
from utils import  get_matched_rows, populate_table


def index(request):
    documents = Document.objects.all()
    return render(request, 'home/home.html', { 'documents': documents })


def analyze(request):
    return render(request, 'home/analyze.html')


def report(request, report_id):
    report_id = int(report_id)
    result = {'report_id': report_id}
    unique_funds = list(Transactions.objects.all().values_list('fund', flat=True).distinct())
    unique_institutions = list(Transactions.objects.all().values_list('account', flat=True).distinct())
    
    if report_id == 1:
        for fund in unique_funds:
            for institution in unique_institutions:
                required_fund = Transactions.objects.filter(fund=fund, account=institution)
                required_institution = ClientData.objects.filter(fund=fund, institution=institution)
                rows = get_matched_rows(required_fund, required_institution)
                result[institution] = rows

        return render(request, 'home/report.html', result)
    elif report_id == 2:
        return render(request, 'home/report.html', result)
    elif report_id == 3:
        return render(request, 'home/report.html', result)
    return render(request, 'home/report.html', result)


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file_name = Document.objects.all().order_by('-uploaded_at').first().document.name
            file_type = form.cleaned_data['file_type']
            file_path = '{media}/{file_name}'.format(media=settings.MEDIA_ROOT, file_name=file_name)
            populate_table(request, file_path, file_type)
            return redirect('index')
    else:
        form = DocumentForm()
    return render(request, 'home/file_upload.html', {'form': form})


def delete(request):
    if request.method == 'POST':
        form = DeleteDataHistoryForm(request.POST)
        
        if form.is_valid():
            models = [Balance, ClientData, Document, Transactions]
            for model in models:
                model_objects = model.objects.all()
                model_objects.delete()

            form.save()
            try:
                shutil.rmtree(settings.MEDIA_ROOT + '/documents')
            except OSError:
                pass
            return redirect('index')
    else:
        form = DeleteDataHistoryForm()
    return render(request, 'home/delete.html', {'form': form})
