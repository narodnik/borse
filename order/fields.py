from django.db import models

class AmountField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 40
        kwargs['decimal_places'] = 20
        super().__init__(*args, **kwargs)

class StatusType:
    ACTIVE = 'Active'
    PROCESSING = 'Process'
    CLOSED = 'Closed'
    CANCELLED = 'Cancel'

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PROCESSING, 'Processing'),
        (CLOSED, 'Closed'),
        (CANCELLED, 'Cancelled')
    )

class StatusField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        kwargs['choices'] = StatusType.STATUS_CHOICES
        super().__init__(*args, **kwargs)

class AccountEventType:
    DEPOSIT = 'DE'
    WITHDRAW = 'WI'

    EVENT_CHOICES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw')
    )

class AccountEventField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = AccountEventType.EVENT_CHOICES
        super().__init__(*args, **kwargs)

class OrderType:
    BUY = 'Buy'
    SELL = 'Sell'

    ORDER_CHOICES = (
        (BUY, 'Buy'),
        (SELL, 'Sell')
    )

class OrderEventField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 4
        kwargs['choices'] = OrderType.ORDER_CHOICES
        super().__init__(*args, **kwargs)

