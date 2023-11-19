from django.urls import path

from .views.auth import *
from .views.test import *
from .views.users import *
from .views.transactions import *

urlpatterns = [
    path('auth/sign_up', sign_up),
    path('auth/login', login),
    path('user/name', get_username),
    path('user/exists', is_user_exists),
    path('delete_all', delete_all),
    path('balance', get_balance),
    path('transaction/create', create_transaction),
]