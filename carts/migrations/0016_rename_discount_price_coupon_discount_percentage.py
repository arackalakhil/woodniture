# Generated by Django 3.2.14 on 2022-08-02 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0015_alter_productoffer_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='discount_price',
            new_name='discount_percentage',
        ),
    ]
