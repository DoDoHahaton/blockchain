import dotenv

import os
from hashlib import sha256
from django.db import models
from dotenv import load_dotenv

from blockchain.models_dir.User import User

load_dotenv()


class Block(models.Model):
    index = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=70)
    previous_hash = models.CharField(max_length=70)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Block №{self.index} hash: {self.hash} previous_hash: {self.previous_hash}'

    def hash__(self, save=False):
        fields = []
        for field in self._meta.fields:
            if field.name != 'index' and field.name != 'hash':
                fields.append(field.value_to_string(self))

        fields += [str(trns) for trns in self.transaction_set.all()]
        block_hash = sha256((str(self.index) + ''.join(fields)).encode()).hexdigest()

        if save:
            self.hash = block_hash
            self.save()

        return block_hash

    @classmethod
    def create(cls):
        print(cls.is_chain_valid())
        if not cls.is_chain_valid():
            return

        if not cls.is_last_filled():
            return

        hash_last = cls.last().hash__()
        Block(previous_hash=hash_last).save()
        return

    @classmethod
    def is_last_filled(cls) -> bool:
        if len(cls.last().transaction_set.all()) >= int(os.getenv('BLOCK_TRANSACTION_COUNT')):
            return True
        return False

    @classmethod
    def is_chain_valid(cls) -> bool:
        blocks = Block.objects.all().order_by('-pk')
        # print([str(blk) for blk in blocks])
        pointer = 0

        while pointer != len(blocks)-1:
            if blocks[pointer].previous_hash != blocks[pointer+1].hash__():
                return False

            pointer += 1
        return True

    @classmethod
    def last(cls):
        last_block = Block.objects.all().order_by('pk').last()

        if not last_block:
            Block(
                previous_hash='GENESIS'
            ).save()

            return cls.last()

        return last_block

    @classmethod
    def delete_all(cls):
        Block.objects.all().delete()


class Transaction(models.Model):
    block = models.ForeignKey(Block, on_delete=models.PROTECT)
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.PROTECT)
    recipient = models.ForeignKey(User, related_name='received_transactions', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.pk}'

    @classmethod
    def create(cls, sender, recipient, amount):
        print(Block.is_last_filled())
        if Block.is_last_filled():
            Block.create()

        last_block = Block.last()

        Transaction.objects.create(
            block=last_block,
            sender=sender,
            recipient=recipient,
            amount=amount
        )

        last_block.hash__(save=True)

    @classmethod
    def delete_all(cls):
        Transaction.objects.all().delete()
