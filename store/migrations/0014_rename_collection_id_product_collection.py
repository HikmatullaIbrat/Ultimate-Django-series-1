# Generated by Django 4.1.2 on 2022-12-30 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_order_cutomer_order_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='collection_id',
            new_name='collection',
        ),
    ]