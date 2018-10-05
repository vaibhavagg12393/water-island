# -*- coding: utf-8 -*-

import shutil

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

from home.forms import DeleteDataHistoryForm, DocumentForm
from home.models import Balance, ClientData, CommentsData, Document, Transactions
from utils import  delete_file, get_matched_balances, get_matched_transactions, populate_table

TRANSACTION = 'transaction'
BALANCE = 'balance'
FILE_TYPE = {TRANSACTION: 'T', BALANCE: 'B'}


class IndexView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['documents'] = Document.objects.all()
        return context


class FeatureView(TemplateView):
    template_name = "home/features.html"


class AnalyzeView(TemplateView):
    template_name = "home/analyze.html"

@csrf_exempt
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
                rows = get_matched_transactions(required_fund, required_institution, report_id)
                result[institution] = rows
    elif report_id == 2:
        for fund in unique_funds:
            for institution in unique_institutions:
                required_fund = Transactions.objects.filter(fund=fund, account=institution)
                required_institution = ClientData.objects.filter(fund=fund, institution=institution)
                rows = get_matched_transactions(required_fund, required_institution, report_id)
                result[institution] = rows
    elif report_id == 3:
        for fund in unique_funds:
            for institution in unique_institutions:
                required_fund = Balance.objects.filter(fund=fund, institution=institution)
                required_institution = ClientData.objects.filter(fund=fund, institution=institution)
                rows = get_matched_balances(required_fund, required_institution, report_id)
                result[institution] = rows
    return render(request, 'home/report.html', result)


def model_form_upload(request):
    error = {}
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file_name = Document.objects.all().order_by('-uploaded_at').first().document.name
            file_type = form.cleaned_data['file_type']
            if (TRANSACTION in file_name.lower() and FILE_TYPE.get(TRANSACTION) != file_type) or (BALANCE in file_name.lower() and FILE_TYPE.get(BALANCE) != file_type):
                error = {'msg': 'Looks like you selected a wrong file type. Please verify that the file type is correct.'}
                delete_file(file_name)
                return render(request, 'home/file_upload.html', {'form': form, 'error': error})
            form.save()
            file_path = '{media}/{file_name}'.format(media=settings.MEDIA_ROOT, file_name=file_name)
            try:
                populate_table(request, file_path, file_type)
            except ValueError:
                error = {'msg': 'Looks like you selected a wrong file type. Please verify that the file type is correct.'}
                delete_file(file_name)
                return render(request, 'home/file_upload.html', {'form': form, 'error': error})

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

@csrf_exempt
def parse_data(request):
    client_id = request.POST.get('id')
    report_id = request.POST.get('reportid')
    comment_text = request.POST.get('commenttext')
    comment, created = CommentsData.objects.update_or_create(client_id=client_id, comment=comment_text, report_id=report_id)
    return JsonResponse(comment.to_dict())
