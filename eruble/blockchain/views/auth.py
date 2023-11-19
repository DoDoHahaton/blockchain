import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from blockchain.dataclasses.responses import Body, Status
from blockchain.models_dir.User import User


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST
        )

    body = json.loads(request.body.decode('utf-8'))

    inn = body.get('inn')
    password = body.get('password')
    print(inn, password)

    if not (inn and password):
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID
        )

    valid = User.login(inn, password)
    if not valid:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED
        )

    return JsonResponse(
        data=Body.AUTHORIZED_TRUE,
        status=Status.OK
    )


@csrf_exempt
def sign_up(request):
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
    created = User.create(body)
    # print(created)
    if not created:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED
        )

    return JsonResponse(
        data=Body.AUTHORIZED_TRUE,
        status=Status.CREATED
    )
