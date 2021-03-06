import os
from datetime import datetime

from django.conf import settings
from pyexcel_xls import get_data

from home.models import Balance, CommentsData, ClientData, Document, Transactions

TRADAR = 'Tradar'
LG = 'LG'
GS = 'GS'
SS = SSB = 'SS'
FUND = {'LITMAN GREGORY': 'LG', 'Y76E': 'LG', 'LG': 'LG'}
INSTITUTION = {'SS': 'SS', 'SSB': 'SS', 'GS': 'GS'}
TRANSACTION_FILE = u'T'
BALANCE_FILE = u'B'


def populate_table(request, file_path, file_type):
    data = get_data(file_path)
    if TRADAR in file_path:
        if file_type == TRANSACTION_FILE:
            for key in data.keys():
                data = data[key]
                for value in data[1:]:
                    try:
                        trade, fund, type, amount, security_type, ticker, isin, cusip, sedol, description, price, date, ccy, settles, account, cash_flow = value[:16]
                        Transactions.objects.create(
                            trade=trade,
                            fund=fund,
                            type=type,
                            amount=amount,
                            security_type=security_type,
                            ticker=ticker,
                            isin=isin,
                            cusip=cusip,
                            sedol=sedol,
                            description=description,
                            price=price,
                            date=date,
                            ccy=ccy,
                            settles=settles,
                            account=account,
                            cash_flow=cash_flow
                        )
                    except ValueError:
                        raise ValueError

        elif file_type == BALANCE_FILE:
            try:
                fund = LG
                institution = GS
                for key in data.keys():
                    data = data[key]
                    for value in data[1:]:
                        if len(value) == 1:
                            fund = FUND.get(value[0])
                        elif len(value) == 2:
                            fund = fund
                            institution = INSTITUTION.get(value[1])
                        elif len(value) == 14:
                            fund = fund
                            institution = institution
                            ccy = value[2]
                        elif len(value) == 15:
                            type, balance = value[4], value[14]
                            Balance.objects.create(
                                fund=fund,
                                institution=institution,
                                ccy=ccy,
                                type=type,
                                balance=balance
                            )
            except ValueError:
                raise ValueError
    else:
        try:
            for key in data.keys():
                data = data[key]
                for value in data[1:]:
                    if value:
                        details = value
                        if file_type == TRANSACTION_FILE:
                            if GS in file_path and len(value) > 15:
                                fund = FUND.get(value[1].upper(), 'LG')
                                institution = u'GS'
                                currency = value[2]
                                amount = value[15]
                                settle_date = value[9]
                                ClientData.objects.create(fund=fund, institution=institution, file_type=file_type,
                                    amount=amount, settle_date=settle_date, details=details, currency=currency)
                            elif SS in file_path.upper() or SSB in file_path.upper() and len(value) > 22:
                                fund = FUND.get(value[0].upper(), 'LG')
                                institution = u'SS'
                                currency = value[22]
                                amount = value[14]
                                settle_date = value[20]
                                ClientData.objects.create(fund=fund, institution=institution, file_type=file_type,
                                    amount=amount, settle_date=settle_date, details=details, currency=currency)
                        elif file_type == BALANCE_FILE:
                            if GS in file_path and len(value) > 5 and value[0] != 'Account Number':
                                fund = FUND.get(value[6].upper(), 'LG') if len(value) > 6 else 'LG'
                                institution = u'GS'
                                currency = value[2]
                                amount = value[4]
                                settle_date = value[5]
                                ClientData.objects.create(fund=fund, institution=institution, file_type=file_type,
                                    amount=amount, settle_date=settle_date, details=details, currency=currency)
                            elif (SS in file_path.upper() or SSB in file_path.upper()) and len(value) > 3:
                                fund = FUND.get(value[0].upper(), 'LG')
                                institution = u'SS'
                                currency = value[1]
                                amount = value[2]
                                settle_date = datetime.now()
                                ClientData.objects.create(fund=fund, institution=institution, file_type=file_type,
                                    amount=amount, settle_date=settle_date, details=details, currency=currency)
        except ValueError:
            raise ValueError


def get_matched_transactions(required_funds, required_institutions, report_id):
    result = []
    if not required_funds or not required_institutions:
        return result
    for institution in required_institutions:
        try:
            comment_obj = CommentsData.objects.get(report_id=report_id, client_id=institution.id)
        except:
            comment_obj = None
        institution.comment = comment_obj.comment if comment_obj else None
        match_found = False
        for fund in required_funds:
            if institution.settle_date == fund.settles and institution.amount == fund.cash_flow:
                institution.match = True
                institution.save()
                result.append(institution)
                match_found = True
        if not match_found:
            institution.match = False
            institution.save()
            result.append(institution)
    
    return result


def get_matched_balances(required_funds, required_institutions, report_id):
    result = []
    if not required_funds or not required_institutions:
        return result
    for institution in required_institutions:
        try:
            comment_obj = CommentsData.objects.get(report_id=report_id, client_id=institution.id)
        except:
            comment_obj = None
        institution.comment = comment_obj.comment if comment_obj else None
        match_found = False
        for fund in required_funds:
            if institution.currency == fund.ccy and institution.amount == fund.balance:
                institution.match = True
                institution.save()
                result.append(institution)
                match_found = True
        if not match_found:
            institution.match = False
            institution.save()
            result.append(institution)
    
    return result


def delete_file(file_name):
    document_object = Document.objects.filter(document=file_name).first()
    if document_object:
        document_object.delete()
    if os.path.exists(file_name):
        try:
            os.remove('{media_root}/{file_name}'.format(media_root=settings.MEDIA_ROOT, file_name=file_name))
        except OSError:
            pass