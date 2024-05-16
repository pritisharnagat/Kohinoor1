# Custom pipeline step to set VrUser and is_customer to True
from django.db import transaction

@transaction.atomic
def set_vruser_and_is_customer(strategy, details, user=None, *args, **kwargs):
    if user:
        user.VrUser = True
        user.is_customer = True
        user.save()
