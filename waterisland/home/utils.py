from datetime import datetime

from pyexcel_xls import get_data

from home.models import Balance, ClientData, Transactions

TRADAR = 'Tradar'
GS = 'GS'
SS = SSB = 'SS'
FUND = {'LITMAN GREGORY': 'LG', 'Y76E': 'LG'}
TRANSACTION_FILE = u'T'
BALANCE_FILE = u'B'


def populate_table(request, file_path, file_type):
    data = get_data(file_path)
    if TRADAR in file_path:
        if file_type == TRANSACTION_FILE:
            for key in data.keys():
                data = data[key]
                for value in data[1:]:
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
        elif file_type == BALANCE_FILE:
            for key in data.keys():
                data = data[key]
                for value in data[1:]:
                    trade, type, amount, security_type, ticker, isin, cusip, description, price, date, settles, cash_flow = value[:16]
                    Balance.objects.create(
                        trade=trade,
                        type=type,
                        amount=amount,
                        security_type=security_type,
                        ticker=ticker,
                        isin=isin,
                        description=description,
                        price=price,
                        date=date,
                        settles=settles,
                        cash_flow=cash_flow
                    )
    else:
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


def get_matched_rows(required_funds, required_institutions):
    result = []
    if not required_funds or not required_institutions:
        return result
    for institution in required_institutions:
        for fund in required_funds:
            if institution.settle_date == fund.settles and institution.amount == fund.cash_flow:
                result.append(institution)
    
    return result

