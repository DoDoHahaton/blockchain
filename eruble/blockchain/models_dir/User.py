from hashlib import sha256
from django.db import models
from django import forms


class User(models.Model):
    inn = models.BigIntegerField(primary_key=True)
    name = models.CharField(null=False, max_length=20)
    password = models.CharField(null=False, max_length=150)
    wallet = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    # class Meta:
    #     app_label = 'blockchain'

    @classmethod
    def create(cls, data):
        form = UserForm(data)
        if not form.is_valid():
            return False

        user = form.save(commit=False)

        if cls.exists(user.inn):
            return False

        user.password = cls.make_password(user.password)
        user.save()
        return True

    @classmethod
    def exists(cls, inn):
        user = User.objects.filter(inn=inn).first()
        return user

    @classmethod
    def make_password(cls, password: str):
        return sha256(password.encode('utf-8')).hexdigest()

    @classmethod
    def is_valid(cls, inn: int, password: str):
        user = User.objects.filter(pk=inn).first()
        if not user:
            return False
        if user.password != cls.make_password(password):
            return False
        return True


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('inn', 'name', 'password')
