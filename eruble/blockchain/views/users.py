import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from blockchain.dataclasses.responses import Body, Status
from blockchain.models_dir.User import User


@csrf_exempt
def is_user_exists(request):
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

    inn = body.get('inn')
    exists = User.exists(inn)

    if not exists:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED
        )

    return JsonResponse(
        data=Body.AUTHORIZED_TRUE,
        status=Status.OK
    )


@csrf_exempt
def get_username(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        body = request.POST

    print(body)

    sender_inn = body.get('sender_inn')
    password = body.get('sender_password')
    recipient_inn = body.get('recipient_inn')

    if not (sender_inn and password and recipient_inn):
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID
        )

    login = User.login(sender_inn, password)
    if not login:
        return JsonResponse(
            data=Body.FORBIDDEN,
            status=Status.FORBIDDEN
        )

    return JsonResponse(
        data={
            'name': login.name
        },
        status=Status.OK
    )


@csrf_exempt
def get_balance(request):
    if request.method != 'POST':
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST
        )

    body = json.loads(request.body.decode('utf-8'))

    inn = body.get('inn')
    password = body.get('password')

    user = User.login(inn, password)

    if not user:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED
        )

    return JsonResponse(
        data={
            'balance': user.wallet
        },
        status=Status.OK
    )
