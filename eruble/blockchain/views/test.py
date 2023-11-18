import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from blockchain.dataclasses.responses import Body, Status
from blockchain.models import User
from blockchain.models_dir.Block import Block, Transaction


@csrf_exempt
def login(request):
    body = json.loads(request.body.decode('utf-8'))

    inn = body.get('inn')
    password = body.get('password')
    print(inn, password)

    if not (inn and password):
        return HttpResponse('Все плохо')

    valid = User.is_valid(inn, password)
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
    body = request.POST

    created = User.create(body)
    if not created:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED
        )

    return JsonResponse(
        data=Body.CREATED,
        status=Status.CREATED
    )


@csrf_exempt
def last(request):
    last = Block.last()

    return HttpResponse(last)


@csrf_exempt
def block_create(request):
    Block.create()

    return HttpResponse('все ок')


@csrf_exempt
def delete_all(request):
    Transaction.delete_all()
    Block.delete_all()


@csrf_exempt
def create_trans(request):
    Transaction.create(
        sender=User.objects.get(pk=1),
        recipient=User.objects.get(pk=2),
        amount=12.00
    )

    return HttpResponse('все ок')
