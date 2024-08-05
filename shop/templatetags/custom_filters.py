# custom_filters.py

import re
from django import template
from shop.models import CartItem

register = template.Library()

@register.filter
def contains_whole_words(text, words):
    text = text.lower()
    words = [word.lower() for word in words.split()]
    for word in words:
        # Use regex to check for whole words
        if re.search(r'\b' + re.escape(word) + r'\b', text):
            return True
    return False

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_cart_item_count(user_registration):
    if user_registration:
        return CartItem.objects.filter(cart_id__is_paid=False, cart_id__user_id=user_registration).count()
    return 0
    