# Generated by Django 4.0.5 on 2022-07-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='img',
            field=models.CharField(max_length=300),
        ),
    ]
