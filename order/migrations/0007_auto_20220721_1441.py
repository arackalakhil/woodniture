# Generated by Django 3.2.14 on 2022-07-21 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0006_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]