# Generated by Django 4.2.3 on 2024-07-02 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_cart_total_price_alter_order_shipping_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
