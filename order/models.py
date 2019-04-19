from django.contrib.auth.models import User, UserManager
from django.db import models

from .fields import *

class AccountUser(User):
    objects = UserManager()
    timestamp = models.DateTimeField(auto_now_add=True)
    # user_status = ACTIVE / SUSPENDED / CLOSED .etc
    # default_language = ARABIC / KURDISH / ENGLISH

class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.TextField()
    is_crypto = models.BooleanField()

    def __str__(self):
        return self.code

    @staticmethod
    def initialize():
        currencies = [
            ('BTC', 'Bitcoin', True),
            ('ETH', 'Ethereum', True),
            ('LTC', 'Litecoin', True),
            ('XMR', 'Monero', True),
            ('SYL', 'Syrian Lira', False),
            ('USD', 'US Dollar', False),
            ('EUR', 'Euro', False),
            ('TRY', 'Turkish Lira', False),
            ('IQD', 'Iraqi Dinar', False),
        ]
        for code, name, is_crypto in currencies:
            currency = Currency.objects.create(
                code=code, name=name, is_crypto=is_crypto)
            currency.save()

class Account(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    balance = AmountField()

    def __str__(self):
        return self.currency.code

class AccountEvents(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                related_name='events')
    event = AccountEventField()
    amount = AmountField()
    status = StatusField()
    reference = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)

    quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                     related_name='quote_orders')

    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                      related_name='base_orders')

    price = models.DecimalField(max_digits=8, decimal_places=2)
    amount = AmountField()
    status = StatusField()
    
    order_type = OrderEventField()

    # When first created, order belongs to no trade.
    # Then once fulfilled, an order corresponds to multiple trades
    # In the maker and taker fields.

    created_timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def remaining_amount(self):
        # amount - sum(trades)
        return self.amount

class OrderEvents(models.Model):
    # This is used to cancel open orders
    # There must be a strict barrier between cancelling an open order
    # and the trading engine.

    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='events')
    event_status = StatusField()
    new_order_status = StatusField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Trade(models.Model):
    # An order can be fulfilled by multiple trades
    # Therefore we're using ForeignKey instead of OneToOne
    maker = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='maker_trades')
    taker = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='taker_trades')

    maker_amount = AmountField()
    maker_fee = AmountField()

    taker_amount = AmountField()
    taker_fee = AmountField()

    timestamp = models.DateTimeField(auto_now_add=True)

