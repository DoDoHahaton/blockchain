import decimal
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from blockchain.dataclasses.responses import Body, Status
from blockchain.models_dir.Block import Transaction
from blockchain.models_dir.User import User


@csrf_exempt
def create_transaction(request):
    if request.method != 'POST':
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST
        )

    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        body = request.POST

    print(body)

    sender_inn = body.get('sender_inn')
    password = body.get('sender_password')
    recipient_inn = body.get('recipient_inn')
    amount = body.get('amount')

    if not (sender_inn and password and recipient_inn and amount):
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID
        )

    amount = float(amount)

    try:
        login = User.login(inn=sender_inn, password=password)
        if login:
            sender = login
        else:
            return JsonResponse(
                data=Body.AUTHORIZED_FALSE,
                status=Status.UNAUTHORIZED
            )
        recipient = User.objects.get(pk=recipient_inn)
    except:
        return JsonResponse(
            data={},
            status=Status.CONFLICT
        )

    if not sender.balance >= round(amount, 2):
        return JsonResponse(
            data=Body.NOT_ENOUGH_MONEY,
            status=Status.CONFLICT
        )

    recipient.wallet += decimal.Decimal(amount)
    recipient.save()
    sender.wallet -= decimal.Decimal(amount)
    sender.save()

    Transaction.create(
        sender=sender,
        recipient=recipient,
        amount=amount,
    )

    return JsonResponse(
        data=Body.CREATED,
        status=Status.CREATED
    )
