from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from blockchain.models_dir.Block import Block, Transaction
from blockchain.models_dir.User import User


@csrf_exempt
def delete_all(request):

    Transaction.delete_all()
    User.delete_all()
    Block.delete_all()
