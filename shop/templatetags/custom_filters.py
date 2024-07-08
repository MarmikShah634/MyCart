# custom_filters.py

from django import template
from shop.models import CartItem

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_cart_item_count(user_registration):
    if user_registration:
        return CartItem.objects.filter(cart_id__is_paid=False, cart_id__user_id=user_registration).count()
    return 0