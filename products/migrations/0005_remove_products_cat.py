# Generated by Django 4.0.5 on 2022-07-04 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_cat_categories_products_cats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='cat',
        ),
    ]
