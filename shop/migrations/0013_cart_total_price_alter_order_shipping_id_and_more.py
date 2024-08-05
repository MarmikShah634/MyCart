# Generated by Django 4.2.3 on 2024-07-02 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_remove_order_total_amount_order_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shipping'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order'),
        ),
    ]
