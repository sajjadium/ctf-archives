from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import QueryDict
from django.shortcuts import redirect, resolve_url
from django.views.decorators.http import require_POST, require_GET

from uuid import uuid4

from accmanager.models import AccountModel
from compfestpay2.secret import FLAG, FLAG_PRICE
from transaction.forms import TransactionForm
from transaction.models import TransactionModel

@login_required(login_url='accmanager:login')
@require_POST
def buyflag(req):
    try:
        trx_pwd = req.POST['transaction_password']
        acc = AccountModel.objects.get(username = req.user.username)
        if not check_password(trx_pwd, acc.transaction_password):
            raise Exception('You have entered wrong transaction password.')
        if acc.balance < FLAG_PRICE:
            raise Exception('Sorry, you are not that rich.')
        acc.balance -= FLAG_PRICE
        acc.save()
        messages.success(req, f'Here is your flag: {FLAG}')
    except ValidationError as e:
        messages.error(req, e.message)
    except Exception as e:
        messages.error(req, str(e))
    url_redirect = resolve_url('accmanager:dashboard') + "#flag"
    return redirect(url_redirect)    

@login_required(login_url='accmanager:login')
@require_POST
def create_trx(req):
    try:
        postBody = QueryDict(f'id={uuid4()}&sender={req.user.username}', True)
        postBody.update(req.POST)
        trxForm = TransactionForm(postBody)
        if trxForm.is_valid():
            trxForm.save()
            messages.success(req, 'Transaction successfully created.')
        err = trxForm.errors.as_data()
        for v in err.values():
            raise v[0]
    except ValidationError as e:
        messages.error(req, e.message)
    except Exception as e:
        messages.error(req, str(e))
    url_redirect = resolve_url('accmanager:dashboard') + "#send"
    return redirect(url_redirect)

@login_required(login_url='accmanager:login')
@require_POST
def update_trx(req, id):
    try:
        postBody = QueryDict(f'id={id}', True)
        postBody.update(req.POST)
        transaction = TransactionModel.objects.get(id = id)
        trxForm = TransactionForm(postBody, instance=transaction)
        if trxForm.is_valid():
            trxForm.save(update = True)
            messages.success(req, 'Transaction message successfully modified.')
        err = trxForm.errors.as_data()
        for v in err.values():
            raise v[0]
    except ValidationError as e:
        messages.error(req, e.message)
    except Exception as e:
        messages.error(req, str(e))
    return redirect('history:sent')

@login_required(login_url='accmanager:login')
@require_GET
def delete_trx(req, id):
    try:
        transaction = TransactionModel.objects.get(id = id)
        amount = transaction.amount
        sender = transaction.sender
        recipient = transaction.recipient
        if sender.username != req.user.username:
            raise Exception(f'Failed to cancel. Transaction {transaction.id} is not yours.')
        if recipient.balance < amount:
            raise Exception(f'Failed to cancel. Transaction {transaction.id} is suspicious.')

        sender.balance += amount
        sender.save()
        recipient.balance -= amount
        recipient.save()
        transaction.delete()

        messages.success(req, 'Transaction successfully canceled.')
    except ValidationError as e:
        messages.error(req, e.message)
    except Exception as e:
        messages.error(req, str(e))
    return redirect('history:sent')