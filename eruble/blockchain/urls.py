from django.urls import path
from .views.test import *
urlpatterns = [
    path('auth/sign_up', sign_up),
    path('auth/login', login),
    path('block/create', block_create),
    path('block/last', last),
    path('delete_all', delete_all),
    path('transaction/create', create_trans),
]