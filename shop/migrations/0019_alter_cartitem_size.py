# Generated by Django 4.2.3 on 2024-08-05 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
