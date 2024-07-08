from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Category, Product
from .middleware import CurrentUserMiddleware

@receiver(pre_save, sender=Category)
def update_category_user(sender, instance, **kwargs):
    current_user = CurrentUserMiddleware.get_current_user()
    if instance.pk is None:
        # The category is being created
        instance.created_by = current_user
    else:
        # The category is being modified
        instance.modified_by = current_user

@receiver(pre_save, sender=Product)
def update_category_user(sender, instance, **kwargs):
    current_user = CurrentUserMiddleware.get_current_user()
    if instance.pk is None:
        # The category is being created
        instance.created_by = current_user
    else:
        # The category is being modified
        instance.modified_by = current_user
