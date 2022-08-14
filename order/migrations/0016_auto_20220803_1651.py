# Generated by Django 3.2.14 on 2022-08-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_alter_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='order_product',
            name='quantity',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(max_length=100, null=True),
        ),
    ]