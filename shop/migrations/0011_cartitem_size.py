# Generated by Django 4.2.3 on 2024-07-01 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_cartitem_cart_created_at_alter_cart_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
