from django.db import models

class AmountField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 40
        kwargs['decimal_places'] = 20
        super().__init__(*args, **kwargs)

class StatusTypes:
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
        kwargs['choices'] = StatusTypes.STATUS_CHOICES
        super().__init__(*args, **kwargs)

class AccountEventTypes:
    DEPOSIT = 'DE'
    WITHDRAW = 'WI'

    EVENT_CHOICES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw')
    )

class AccountEventField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = AccountEventTypes.EVENT_CHOICES
        super().__init__(*args, **kwargs)
